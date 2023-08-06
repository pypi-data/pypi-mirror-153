import asyncio
import queue
import signal
import time
from binascii import hexlify
from copy import copy
from typing import List, Dict

import zmq
import zmq.asyncio
from zmq.asyncio import Socket, Poller

import palaestrai.core.MDP as MDP
from . import LOG
from .zhelpers import pprint_message, ContextGuard
from ..store.receiver import StoreReceiver


class Service(object):
    """A single service managed by this broker"""

    def __init__(self, name):
        """Creates a new Service object for a given service name

        :param name: The service name
        """
        self.name = name
        self.requests = []
        self.waiting = []

    def __str__(self):
        return "Service(name=%s, requests=%s, waiting=%s)" % (
            self.name,
            self.requests,
            self.waiting,
        )


class Worker(object):
    """Represents an external Worker in the major domo protocol.

    The major domo protocol knows clients (who send out requests) and workers,
    who process these requests. This internal data structure represents such
    an external worker and is used for bookkeeping.
    """

    def __init__(self, identity, address, lifetime):
        """Create a new worker structure

        :param identity: The hex identity of the worker; can be arbitrary, but
            must be unique
        :param address: The workers TCP connection address
        :param lifetime: How long the worker can stay in the books
        """
        self.service = None
        self.address = address
        self.identity = identity
        self.expiry = time.time() + 1e-3 * lifetime

    def __str__(self):
        return "Worker(identity=%s, address=%s, service=%s, expiry=%s)" % (
            self.identity,
            self.address,
            self.service,
            self.expiry,
        )

    def __repr__(self):
        return str(self)


class MajorDomoBroker:
    """Distributes messages between clients and workers according to services

    This Major Domo Protocol broker is a minimal implementation of
    http:#rfc.zeromq.org/spec:7 and spec:8.
    """

    INTERNAL_SERVICE_PREFIX = b"mmi."
    HEARTBEAT_LIVENESS = 3  # 3-5 is reasonable
    HEARTBEAT_INTERVAL = 2500  # msecs
    HEARTBEAT_EXPIRY = HEARTBEAT_INTERVAL * HEARTBEAT_LIVENESS

    def __init__(self, uri=None):
        """Create a new MajorDomoBroker to listen at a specific URI

        :param uri: The URI the broker should listen on
        """
        self._running: bool = True

        self._uri: str = uri
        self._socket: Socket = None
        self._poller: Poller = None
        self._services: Dict[Service] = {}
        self._workers: Dict[Worker] = {}
        self._waiting: List[Worker] = []
        self._heartbeat_at = (
            time.time() + 1e-3 * MajorDomoBroker.HEARTBEAT_INTERVAL
        )

        self._queue: queue.Queue = None
        self._store_receiver: StoreReceiver = None

        LOG.debug("New MajorDomoBroker(id=0x%x, uri=%s)", id(self), self._uri)

    def _handle_signal_interrupt(self, signum):
        if signum in {signal.SIGABRT, signal.SIGTERM}:
            LOG.debug(
                "MajorDomoBroker(id=0x%x, uri=%s) "
                "received signal %s, terminating",
                id(self),
                self._uri,
                signum,
            )
            self._running = False
        elif signum == signal.SIGINT:
            LOG.debug(
                "MajorDomoBroker(id=0x%x, uri=%s) "
                "staying online after SIGINT for as long as possible "
                "to allow for an orderly shutdown",
                id(self),
                self._uri,
            )
        else:
            LOG.debug(
                "MajorDomoBroker(id=0x%x, uri=%s) "
                "received signal %s, but will ignore it",
                id(self),
                self._uri,
                signum,
            )

    def _init_signal_handler(self):
        signals = {signal.SIGINT, signal.SIGABRT, signal.SIGTERM}
        LOG.debug(
            "MajorDomoBroker(id=0x%x) "
            "registering signal handlers for signals %s",
            id(self),
            signals,
        )
        loop = asyncio.get_running_loop()
        for signum in signals:
            loop.add_signal_handler(
                signum, self._handle_signal_interrupt, signum
            )

    def _init_communication(self):
        self._socket = zmq.asyncio.Socket(
            context=ContextGuard.asyncio_context(), socket_type=zmq.ROUTER
        )  # self.ctx.socket(zmq.ROUTER)
        self._socket.linger = 0
        self._poller = zmq.asyncio.Poller()
        self._poller.register(self._socket, zmq.POLLIN)
        self.bind(self._uri)

    def _init_store(self):
        self._queue = queue.Queue()
        self._store_receiver = StoreReceiver(self._queue)
        self._store_receiver.start()

    async def mediate(self):
        """Mediation loop for message distribution

        This method is an infinite loop that receives and distributes messages
        received from clients and workers.
        """
        LOG.debug(
            "MajorDomoBroker(id=0x%x, uri=%s) "
            "MDP broker/0.1.1 starting mediation",
            id(self),
            self._uri,
        )

        self._init_signal_handler()
        self._init_communication()
        self._init_store()

        LOG.debug(
            "MajorDomoBroker(id=0x%x, uri=%s) "
            "started StoreReceiver(id=0x%x, uid=%s)",
            id(self),
            self._uri,
            id(self._store_receiver),
            self._store_receiver.uid,
        )

        while self._running:
            items = await self._poller.poll(self.HEARTBEAT_INTERVAL)
            if not items or not self._running:
                continue
            msg = await self._socket.recv_multipart()
            msg_dup = copy(msg)
            sender = msg.pop(0)
            empty = msg.pop(0)
            assert empty == b""
            header = msg.pop(0)

            LOG.debug(
                "MajorDomoBroker(id=0x%d, uri=%s) received message "
                "from '%s' of type '%s'",
                id(self),
                self._uri,
                sender,
                header,
            )

            if MDP.C_CLIENT == header:
                if msg[0] == MDP.W_DESTROY:
                    await self._destroy()
                    break
                await self.process_client(sender, msg)
            elif MDP.W_WORKER == header:
                await self._process_worker(sender, msg)
            else:
                LOG.debug(
                    "MajorDomoBroker(id=0x%d, uri=%s) "
                    "received invalid message, ignoring",
                    id(self),
                    self._uri,
                )
            await self.purge_workers()
            await self.send_heartbeats()
            self._queue.put_nowait(msg_dup)  # Process for store.
        self._store_receiver.shutdown()
        self._queue.join()
        self._store_receiver.join()

    async def _destroy(self):
        """Disconnect all workers, destroy context."""
        LOG.debug(
            "MajorDomoBroker(id=0x%d, uri=%s) destroying workers",
            id(self),
            self._uri,
        )
        while self._workers:
            await self._delete_worker(list(self._workers.values())[0], True)

    async def process_client(self, sender, msg):
        """Process a request coming from a client."""
        assert len(msg) >= 2  # Service name + body
        service = msg.pop(0)
        # Set reply return address to client sender
        msg = [sender, b""] + msg
        if service.startswith(self.INTERNAL_SERVICE_PREFIX):
            await self.service_internal(service, msg)
        else:
            await self.dispatch(self._require_service(service), msg)

    async def _process_worker(self, sender, msg):
        """Process message sent to us by a worker."""
        assert len(msg) >= 1  # At least, command
        command = msg.pop(0)

        worker_ready = hexlify(sender) in self._workers
        worker = self.require_worker(sender)

        if MDP.W_READY == command:
            assert len(msg) >= 1  # At least, a service name
            service = msg.pop(0)
            # Not first command in session or Reserved service name
            if worker_ready or service.startswith(
                self.INTERNAL_SERVICE_PREFIX
            ):
                await self._delete_worker(worker, True)
            else:
                # Attach worker to service and mark as idle
                worker.service = self._require_service(service)
                await self.worker_waiting(worker)

        elif MDP.W_REPLY == command:
            if worker_ready:
                # Remove & save client return envelope and insert the
                # protocol header and service name, then rewrap envelope.
                client = msg.pop(0)
                _ = msg.pop(0)  # Empty delimiter frame, see MDP definition
                msg = [client, b"", MDP.C_CLIENT, worker.service.name] + msg
                await self._socket.send_multipart(msg)
                await self.worker_waiting(worker)
            else:
                await self._delete_worker(worker, True)

        elif MDP.W_HEARTBEAT == command:
            if worker_ready:
                worker.expiry = time.time() + 1e-3 * self.HEARTBEAT_EXPIRY
            else:
                await self._delete_worker(worker, True)

        elif MDP.W_DISCONNECT == command:
            await self._delete_worker(worker, False)
        else:
            LOG.error("Broker received invalid message")
            LOG.debug(pprint_message(msg))

    async def _delete_worker(self, worker, disconnect):
        """Deletes worker from all data structures, and deletes worker."""
        assert worker is not None
        if disconnect:
            await self.send_to_worker(worker, MDP.W_DISCONNECT, None, None)

        if worker.service is not None and worker in worker.service.waiting:
            worker.service.waiting.remove(worker)

        if worker.identity not in self._workers:
            LOG.error(
                "Worker identity '%s' is missing in workers %s (dc: %s).",
                worker.identity,
                self._workers,
                str(disconnect),
            )
        self._workers.pop(worker.identity)

    def require_worker(self, address) -> Worker:
        """Finds the worker (creates if necessary)."""
        assert address is not None
        identity = hexlify(address)
        worker = self._workers.get(identity)
        if worker:
            return worker
        worker = Worker(identity, address, self.HEARTBEAT_EXPIRY)
        self._workers[identity] = worker
        LOG.debug(
            "MajorDomoBroker(id=0x%x, uri=%s) "
            "registered new Worker(identity=%s, address=%s)",
            id(self),
            self._uri,
            identity,
            address,
        )
        return worker

    def _require_service(self, name):
        """Locates the service (creates if necessary)."""
        assert name is not None
        service = self._services.get(name)
        if service:
            return service
        service = Service(name)
        self._services[name] = service
        return service

    def bind(self, endpoint):
        """Bind broker to endpoint, can call this multiple times.

        We use a single socket for both clients and workers.
        """
        try:
            self._socket.bind(endpoint)
        except zmq.error.ZMQError as e:
            LOG.fatal(
                "MajorDomoBroker(id=0x%x, uri=%s) " "failed to bind: %s",
                id(self),
                self._uri,
                e,
            )
            raise e
        LOG.debug(
            "MajorDomoBroker(id=0x%x, uri=%s) bound successfully to socket",
            id(self),
            endpoint,
        )

    async def service_internal(self, service, msg):
        """Handle internal service according to 8/MMI specification"""
        returncode = b"501"
        if b"mmi.service" == service:
            name = msg[-1]
            returncode = b"200" if name in self._services else b"404"
        msg[-1] = returncode

        # insert the protocol header and service name
        # after the routing envelope ([client, '']):
        msg = msg[:2] + [MDP.C_CLIENT, service] + msg[2:]
        await self._socket.send_multipart(msg)

    async def send_heartbeats(self):
        """Send heartbeats to idle workers if neccessary.

        This method checks for the current time elapsed being past the next
        designated checkpoint, and if yes, sends a heartbeat message to all
        workers.
        """
        if time.time() <= self._heartbeat_at:
            return
        for worker in self._waiting:
            LOG.debug("Sending heartbeat to worker %s", worker)
            await self.send_to_worker(worker, MDP.W_HEARTBEAT, None, None)
        self._heartbeat_at = time.time() + 1e-3 * self.HEARTBEAT_INTERVAL

    async def purge_workers(self):
        """Look for & kill expired workers."""
        while self._waiting:
            # Workers are stored from oldest to most recent, so we pop
            # until we find an active one.
            w = self._waiting[0]
            if w.expiry >= time.time():
                break
            LOG.info("Broker deleting expired worker: %s", w.identity)
            await self._delete_worker(w, False)
            self._waiting.pop(0)

    async def worker_waiting(self, worker):
        """This worker is now waiting for work."""
        self._waiting.append(worker)
        worker.service.waiting.append(worker)
        worker.expiry = time.time() + 1e-3 * self.HEARTBEAT_EXPIRY
        await self.dispatch(worker.service, None)

    async def dispatch(self, service, msg):
        """Dispatch requests to waiting workers as possible"""
        assert service is not None
        if msg is not None:  # Queue message if any
            service.requests.append(msg)
        await self.purge_workers()
        LOG.debug(
            "MajorDomoBroker(id=0x%x, uri=%s) "
            "is dispatching a message to service '%s'; "
            "Services: %s %s, Workers: %s %s",
            id(self),
            self._uri,
            service,
            len(self._services.keys()),
            self._services.keys(),
            len(self._workers.keys()),
            self._workers,
        )
        while service.waiting and service.requests:
            msg = service.requests.pop(0)
            worker = service.waiting.pop(0)
            self._waiting.remove(worker)
            await self.send_to_worker(worker, MDP.W_REQUEST, None, msg)

    async def send_to_worker(self, worker, command, option, msg=None):
        """Send message to worker.

        If message is provided, sends that message.
        """
        if msg is None:
            msg = []
        elif not isinstance(msg, list):
            msg = [msg]

        # Stack routing and protocol envelopes to start of message
        # and routing envelope
        if option is not None:
            msg = [option] + msg
        msg = [worker.address, b"", MDP.W_WORKER, command] + msg
        LOG.debug(
            "MajorDomoBroker(id=0x%x, uri=%s) "
            "sending message with command '%r' to '%s'",
            id(self),
            self._uri,
            command,
            worker,
        )
        await self._socket.send_multipart(msg)

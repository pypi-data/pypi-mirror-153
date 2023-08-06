"""Majordomo Protocol Worker API, Python version
Implements the MDP/Worker spec at http:#rfc.zeromq.org/spec:7.
Author: Min RK <benjaminrk@gmail.com>
Based on Java example by Arkadiusz Orzechowski
"""

import time

import zmq
import zmq.asyncio

import palaestrai.core.MDP as MDP
from . import LOG
from .serialisation import deserialize, serialize
from .zhelpers import pprint_message, ContextGuard


class MajorDomoWorker:
    """A task receiver with heartbeats

    The Major Domo Worker connects to a broker and listens to requests
    to designated service. Thiese it picks up, returns them to the calling
    loop, and also sends replies. The worker has a separate heartbeat to find
    out whether the connection to the broker has become stale.

    This is the Major Domo Protocol Worker API, Python version.
    Implements the MDP/Worker spec at http:#rfc.zeromq.org/spec:7.
    """

    HEARTBEAT_LIVENESS = 3  # 3-5 is reasonable
    DEFAULT_HEARTBEAT_DELAY = 2500  # Heartbeat delay, msecs
    reconnect = 2500  # Reconnect delay, msecs
    timeout = 2500  # poller timeout

    def __init__(self, broker_uri: str, service):
        self._socket = None
        self._broker_uri = broker_uri
        if isinstance(service, str):
            self._service = bytes(service, "ascii")
        elif isinstance(service, bytes):
            self._service = service
        else:
            self._service = bytes(str(service), "ascii")
        self._reply_to = None
        self._expect_reply = False
        self._poller = zmq.asyncio.Poller()
        self._liveness = 0
        self._heartbeat_at = 0
        self.heartbeat_delay = MajorDomoWorker.DEFAULT_HEARTBEAT_DELAY

    async def _connect(self):
        """Connect or reconnect to broker"""
        if self._socket:
            self._poller.unregister(self._socket)
            self._socket.close()
        self._socket = zmq.asyncio.Socket(
            context=ContextGuard.asyncio_context(), socket_type=zmq.DEALER
        )
        self._socket.linger = 0
        self._socket.connect(self._broker_uri)
        self._poller.register(self._socket, zmq.POLLIN)
        LOG.debug(
            "MajorDomoWorker(id=0x%x, service=%s, broker_uri=%s) "
            "connecting to MajorDomoBroker",
            id(self),
            self._service,
            self._broker_uri,
        )

        # Register service with broker
        await self._send(MDP.W_READY, self._service, [])

        # If liveness hits zero, queue is considered disconnected
        self._liveness = self.HEARTBEAT_LIVENESS
        self._heartbeat_at = time.time() + 1e-3 * self.heartbeat_delay

    async def _send(self, command, option=None, msg=None):
        """Send message to broker.
        If no msg is provided, creates one internally
        """

        if not self._socket:
            await self._connect()

        if msg is None:
            msg = []
        elif not isinstance(msg, list):
            msg = [msg]
        if option:
            msg = [option] + msg

        LOG.debug(
            "MajorDomoWorker(id=0x%x, service=%s, uri=%s) "
            "sending to broker: %s",
            id(self),
            self._service,
            self._broker_uri,
            msg,
        )
        msg = [b"", MDP.W_WORKER, command] + msg
        await self._socket.send_multipart(msg)

    async def transceive(self, reply=None, skip_recv=False):
        """Send and receive main method of the major domo worker

        This method does it both: First, it sends a reply to the last message
        that was recived --- the major domo worker keeps track of that ---,
        then it waits for the next message. This is the normal operation.

        There can be exceptions, which are only sensible for the first or
        the last message. One can skip sending a reply, which is sensible for
        the very first message (`reply=None`), or one can skip the receiving
        part (`skip_recv=True`), which is sensible when the parent object of
        the worker shuts down and sends its last ACK.

        :param reply: The reply to send to the last message received.
        :param skip_recv: If `True`, the worker will only send and skip the
            receiving part.
        :return: A message body in serialized form
        """
        LOG.debug(
            "MajorDomoWorker(id=0x%x, broker_uri=%s, service=%s) "
            "in recv(reply=%s, skip_recv=%s), starting to poll",
            id(self),
            self._broker_uri,
            self._service,
            reply,
            skip_recv,
        )
        if reply is None and self._expect_reply:
            LOG.error(
                "MajorDomoWorker(id=%s, broker_uri=%s, service=%s) "
                "is expected to send a reply, but has none on recv; cowardly"
                "refusing to continue",
                id(self),
                self._broker_uri,
                self._service,
            )
            return

        if reply:
            assert not isinstance(reply, bytes)
            reply = serialize(reply)
            if not isinstance(reply, list):
                reply = [reply]
            reply = [self._reply_to, b""] + reply
            await self._send(MDP.W_REPLY, msg=reply)
        self._expect_reply = True  # We may recv only once without reply.

        if skip_recv:
            return
        while True:
            # Poll socket for a reply, with timeout
            try:
                LOG.debug(
                    "MajorDomoWorker(id=0x%x, service=%s, broker_uri=%s) "
                    "waiting for messages",
                    id(self),
                    self._service,
                    self._broker_uri,
                )
                items = await self._poller.poll(self.timeout)
            except KeyboardInterrupt:
                break  # Interrupted

            if items:
                msg = await self._socket.recv_multipart()
                LOG.debug(
                    "MajorDomoWorker(id=0x%x, service=%s, broker_uri=%s) "
                    "received message from broker: %s",
                    id(self),
                    self._service,
                    self._broker_uri,
                    pprint_message(msg),
                )

                self._liveness = self.HEARTBEAT_LIVENESS
                # Don't try to handle errors, just assert noisily
                if len(msg) < 3:
                    LOG.error(
                        "MajorDomoWorker(id=0x%x, service=%s, "
                        "broker_uri=%s) "
                        "of length = %d, should be >= 3; ignoring",
                        id(self),
                        self._service,
                        self._broker_uri,
                        len(msg),
                    )
                    continue
                empty = msg.pop(0)
                if empty != b"":
                    LOG.error(
                        "MajorDomoWorker(id=0x%x, service=%s, "
                        "broker_uri=%s) received message that "
                        "violates the MDP: empty != ''",
                        id(self),
                        self._service,
                        self._broker_uri,
                    )
                    continue
                header = msg.pop(0)
                if header != MDP.W_WORKER:
                    LOG.error(
                        "MajorDomoWorker(id=0x%x, service=%s, "
                        "broker_uri=%s) received header '%s', but expected"
                        " '%s'; ignoring message",
                        id(self),
                        self._service,
                        self._broker_uri,
                        header,
                        MDP.W_WORKER,
                    )
                    continue

                command = msg.pop(0)
                if command == MDP.W_REQUEST:
                    # We should pop and save as many addresses as there are
                    # up to a null part, but for now, just save one...
                    self._reply_to = msg.pop(0)
                    # pop empty
                    empty = msg.pop(0)
                    assert empty == b""

                    return deserialize(msg)  # We have a request to process

                elif command == MDP.W_HEARTBEAT:
                    # Do nothing for heartbeats
                    pass
                elif command == MDP.W_DISCONNECT:
                    await self._connect()
                else:
                    LOG.error(
                        "MajorDomoWorker(id=0x%x, service=%s, "
                        "broker_uri=%s) "
                        "received invalid input message: %s",
                        id(self),
                        self._service,
                        self._broker_uri,
                        pprint_message(msg),
                    )
            else:
                self._liveness -= 1
                if self._liveness <= 0:
                    if self._socket:  # Reconnect: sleep a bit
                        LOG.warning(
                            "MajorDomoWorker(id=0x%x, service=%s, uri=%s) "
                            "disconnected from broker, reconnecting",
                            id(self),
                            self._service,
                            self._broker_uri,
                        )
                        try:
                            time.sleep(1e-3 * self.reconnect)
                        except KeyboardInterrupt:
                            break
                    await self._connect()

            # Send HEARTBEAT if it's time
            if time.time() > self._heartbeat_at:
                await self._send(MDP.W_HEARTBEAT)
                self._heartbeat_at = time.time() + 1e-3 * self.heartbeat_delay
        LOG.warning("Worker received interrupt, committing seppuku")
        return None

    def disconnect(self):
        """Disconnects the worker from the broker."""
        self._send(MDP.W_DISCONNECT)

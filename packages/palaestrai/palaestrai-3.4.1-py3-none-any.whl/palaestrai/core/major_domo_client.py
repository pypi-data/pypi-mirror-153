""""Majordomo Protocol Client API, Python version.
Implements the MDP/Worker spec at http:#rfc.zeromq.org/spec:7.
Author: Min RK <benjaminrk@gmail.com>
Based on Java example by Arkadiusz Orzechowski
"""

import zmq
import zmq.asyncio

from . import LOG, MDP
from .runtime_config import RuntimeConfig
from .serialisation import deserialize, serialize
from .zhelpers import ContextGuard


class MajorDomoClient:
    """Client object for distributing tasks to workers and receiving results

    The major domo protocol client is the initiator of tasks. It sends
    messages that are distributed according to a service name to worksers. The
    main method of this class, :py:func:`MajorDomoClient.send`, sends such
    a request and waits for the reply of the corresponding worker.

    Major domo clients strictly adhere to the request-response pattern:
    A client always awaits for a reply when sending a request.

    Majordomo Protocol Client API, Python version.
    Implements the MDP/Worker spec at http:#rfc.zeromq.org/spec:7.
    """

    def __init__(self, broker_uri: str):
        self._socket = None
        self._broker_uri = broker_uri
        self._poller = zmq.asyncio.Poller()
        self.timeout = RuntimeConfig().major_domo_client_timeout
        self.retries = RuntimeConfig().major_domo_client_retries

    def reconnect_to_broker(self):
        """Connect or reconnect to broker

        Attempts to connect to the broker. This method can be called multiple
        times: For initial connection, or for reconnection.
        """

        if self._socket:
            self._poller.unregister(self._socket)
            self._socket.close()
        self._socket = zmq.asyncio.Socket(
            context=ContextGuard.asyncio_context(), socket_type=zmq.REQ
        )  # self.ctx.socket(zmq.REQ)
        self._socket.linger = 0
        self._socket.connect(self._broker_uri)
        self._poller.register(self._socket, zmq.POLLIN)
        LOG.debug(
            "MajorDomoClient(id=%s) connected to MajorDomoBroker(uri=%s)",
            id(self),
            self._broker_uri,
        )

    async def destroy(self):
        if not self._socket:
            self.reconnect_to_broker()
        request = [MDP.C_CLIENT, MDP.W_DESTROY]
        LOG.debug(
            "MajorDomoClient(id=%s) sending destroy message "
            "to MajorDomoBroker(uri=%s)",
            id(self),
            self._broker_uri,
        )
        await self._socket.send_multipart(request)

    async def send(self, service, request):
        """Send request to broker and get reply by hook or crook.

        Takes ownership of request message and destroys it when sent.
        Returns the reply message or None if there was no reply.
        """
        assert not isinstance(request, bytes)
        request = serialize(request)

        if not isinstance(service, bytes):
            service = bytes(str(service), "ascii")

        if not self._socket:
            self.reconnect_to_broker()

        if not isinstance(request, list):
            request = [request]
        request = [MDP.C_CLIENT, service] + request

        retries = self.retries
        while retries > 0:
            LOG.debug(
                "MajorDomoClient(id=%s) sending request to service '%s'",
                id(self),
                service,
            )
            await self._socket.send_multipart(request)
            try:
                items = await self._poller.poll(self.timeout)
            except KeyboardInterrupt:
                return None
            except SystemExit:
                return None
            if items:
                msg = await self._socket.recv_multipart()
                LOG.debug("MajorDomoClient(id=%s) received reply", id(self))

                if len(msg) < 3:
                    LOG.error(
                        "MajorDomoClient(id=0x%x) received message "
                        "of length = %d, should be >= 3; ignoring",
                        id(self),
                        len(msg),
                    )
                    break
                header = msg.pop(0)
                if header != MDP.C_CLIENT:
                    LOG.error(
                        "MajorDomoClient(id=0x%x) received message "
                        "with header type '%s', but expected '%s'; ignoring",
                        id(self),
                        header,
                        MDP.C_CLIENT,
                    )
                    break

                reply_service = msg.pop(0)
                if service != reply_service:
                    LOG.error(
                        "MajorDomoClient(id=0x%x) received reply "
                        "for service '%s', but waited for service '%s'; "
                        "returning for the caller to enjoy the unwanted gift",
                        id(self),
                        service,
                        reply_service,
                    )
                return deserialize(msg)
            else:
                if retries:
                    LOG.warning(
                        "MajorDomoClient(id=%s) "
                        "received no response from service '%s' "
                        "for message %s "
                        "after %s of %s attempt(s) with timeout %s, "
                        "reconnecting and retrying",
                        id(self),
                        service,
                        str(request),
                        self.retries - retries,
                        self.retries,
                        self.timeout,
                    )
                    self.reconnect_to_broker()
                else:
                    LOG.error(
                        "MajorDomoClient(id=0x%x) suffering from permanent "
                        "connection error: Tried service '%s' %s times, "
                        "but got no response for request %s, "
                        "abondoning this message",
                        id(self),
                        service,
                        self.retries,
                        str(request),
                    )
                    break
                retries -= 1
        return None

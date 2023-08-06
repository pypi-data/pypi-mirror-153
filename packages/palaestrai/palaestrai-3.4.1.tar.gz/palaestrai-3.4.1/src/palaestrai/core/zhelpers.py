# encoding: utf-8
"""
Helper module for example applications. Mimics ZeroMQ Guide's zhelpers.h.
"""

from __future__ import print_function

import binascii
import os
import socket
from random import randint

import zmq
import zmq.asyncio


def socket_set_hwm(socket, hwm=-1):
    """libzmq 2/3/4 compatible sethwm"""
    try:
        socket.sndhwm = socket.rcvhwm = hwm
    except AttributeError:
        socket.hwm = hwm


def pprint_message(msg):
    """Pretty-prints a message to a string.

    :param msg: A message of the palaestrai zmq core protocol
    :return: The pretty-printed message
    """

    def str_or_hex(p):
        try:
            return p.decode("ascii")
        except UnicodeDecodeError:
            return r"0x%s" % binascii.hexlify(p).decode("ascii")

    return "\n".join(
        ["[%03d] %s" % (len(p), str_or_hex(p)) for p in [x for x in msg]]
    )


def dump(msg_or_socket):
    """Receives all message parts from socket, printing each frame neatly"""
    if isinstance(msg_or_socket, zmq.Socket):
        # it's a socket, call on current message
        msg = msg_or_socket.recv_multipart()
    else:
        msg = msg_or_socket
    print("----------------------------------------")
    for part in msg:
        print("[%03d]" % len(part), end=" ")
        is_text = True
        try:
            print(part.decode("ascii"))
        except UnicodeDecodeError:
            print(r"0x%s" % (binascii.hexlify(part).decode("ascii")))


def set_id(zsocket):
    """Set simple random printable identity on socket"""
    identity = "%04x-%04x" % (randint(0, 0x10000), randint(0, 0x10000))
    zsocket.setsockopt_string(zmq.IDENTITY, identity)


def zpipe(ctx):
    """build inproc pipe for talking to threads
    mimic pipe used in czmq zthread_fork.
    Returns a pair of PAIRs connected via inproc
    """
    a = ctx.socket(zmq.PAIR)
    b = ctx.socket(zmq.PAIR)
    a.linger = b.linger = 0
    a.hwm = b.hwm = 1
    iface = "inproc://%s" % binascii.hexlify(os.urandom(8))
    a.bind(iface)
    b.connect(iface)
    return a, b


class _ContextGuard:
    """Guards ZMQ contexts: Creates exactly one per process

    This guard class makes sure that only ever one ZMQ Context is created per
    process. It automagically creates a new one when there's a need to (e.g.,
    after fork()), but returns the current one otherwise.
    """

    def __init__(self):
        self._id = None
        self._context = None
        self._asyncio_context = None

    @staticmethod
    def _generate_id():
        return "%s@%s" % (os.getpid(), socket.gethostname())

    def _update_contexts(self):
        fresh_id = self._generate_id()
        if not self._context or not self._id or self._id != fresh_id:
            self._id = fresh_id
            self._context = zmq.Context()
            self._asyncio_context = zmq.asyncio.Context()

    def context(self):
        self._update_contexts()
        return self._context

    def asyncio_context(self):
        self._update_contexts()
        return self._asyncio_context


ContextGuard = _ContextGuard()

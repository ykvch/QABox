#!/usr/bin/env python
# coding: utf-8

"""Stateful server based on python3 asyncio callback interface"""

import asyncio


# Each client connection will create a new protocol instance
class Proto(asyncio.Protocol):

    def __init__(self, master):
        print("Proto created")
        self.master = master
        super(Proto, self).__init__()

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        if message.splitlines()[0] == "Done":
            print('Got magic word')
            print('Close the client socket')
            self.transport.close()  # Important, server won't close otherwise
            self.master.server.close()
            return

        print('Send: {!r}'.format(message))
        self.transport.write(data)


# Enable Proto access to common server instance
class RegServer:
    def __init__(self, proto, host, port, loop):
        self.host, self.port = host, port
        self.proto = proto
        self.loop = loop
        self.server = loop.run_until_complete(
            loop.create_server(self.proto_factory, host, port))

    def proto_factory(self):
        return self.proto(self)


loop = asyncio.get_event_loop()

# creator = loop.create_server(Proto, '127.0.0.1', 8888)
# loop.create_task(creator)
# server = loop.run_until_complete(loop.create_task(creator))
# server = loop.run_until_complete(creator)

reg = RegServer(Proto, '127.0.0.1', 8888, loop)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(reg.server.sockets[0].getsockname()))
try:
    loop.run_until_complete(reg.server.wait_closed())
except KeyboardInterrupt:
    reg.server.close()

loop.run_until_complete(reg.server.wait_closed())
loop.close()

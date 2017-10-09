# coding: utf-8

import asyncio
import argparse


COMMANDS = {}


def command(*args):
    """Decorator to set functions as commands for server"""
    def wrap(f):
        for i in args:
            COMMANDS[i] = f
        return f
    return wrap


@command("nodes")
async def nodes():
    for k, v in server._nodes.items():
        yield("{} {}".format(k, len(v)))


@command("thank")
async def done(*args):
    """Stop the server"""
    server.time2stop = True
    yield ""


@command("echo")
async def echo(*args):
    """Simple echo command to print back params"""
    yield " ".join(args)


@command("h", "help")
def help(*args):
    """Print help message"""
    if args and args[0] in COMMANDS:
        return COMMANDS[args[0]].__doc__
    return "Available commands: " + " ".join(COMMANDS.keys())


async def _dispatch(cmd, args):
    async for i in COMMANDS.get(cmd, help)(*args):
        yield bytes((str(i) + "\n").encode())


async def handle_command(reader, writer):
    buff = ""

    data = await reader.read(1024)
    message = data.decode()

    while message:
        head, sep, tail = message.partition("\n")
        buff += head

        while sep:
            cmd, *params = buff.split(" ")
            async for i in _dispatch(cmd, params):
                writer.write(i)
            if server.time2stop:
                writer.close()
                server.close()
            buff, sep, tail = tail.partition("\n")

        data = await reader.read(1024)
        message = data.decode()

    print("Close the client socket")
    writer.close()


# Parse command line arguments
parser = argparse.ArgumentParser(description="Server part of test registry plugin",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-a", "--address", default="127.0.0.1", help="Listen address")
parser.add_argument("-p", "--port", type=int, default=8888, help="Listen port")
args = parser.parse_args()

loop = asyncio.get_event_loop()
server = loop.run_until_complete(
    asyncio.start_server(handle_command, args.address, args.port, loop=loop))
server.time2stop = False  # stop flag
server._nodes = {"a": "qwer"}  # {node: [taken_files_list],...}

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_until_complete(server.wait_closed())
except KeyboardInterrupt:
    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())

loop.close()

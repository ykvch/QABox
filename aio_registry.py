# coding: utf-8

import asyncio


COMMANDS = {}


def command(*args):
    def wrap(f):
        for i in args:
            COMMANDS[i] = f
        return f
    return wrap


@command("echo")
def echo(*args):
    """Simple echo command to print back params"""
    return " ".join(args)


@command("h", "help")
def help(*args):
    """Print help message"""
    if args and args[0] in COMMANDS:
        return COMMANDS[args[0]].__doc__
    return "Available commands: " + " ".join(COMMANDS.keys())


def dispatch(cmd, args):
    retval = str(COMMANDS.get(cmd, help)(*args)) + "\n"
    return bytes(retval.encode())


async def handle_command(reader, writer):
    buff = ""

    data = await reader.read(7)
    message = data.decode()

    while message:
        head, sep, tail = message.partition("\n")
        buff += head

        while sep:
            cmd, *params = buff.split(" ")
            writer.write(dispatch(cmd, params))
            buff, sep, tail = tail.partition("\n")

        data = await reader.read(7)
        message = data.decode()
        continue

    print("Close the client socket")
    writer.close()

loop = asyncio.get_event_loop()

server = loop.run_until_complete(
    asyncio.start_server(handle_command, '127.0.0.1', 8888, loop=loop))

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()

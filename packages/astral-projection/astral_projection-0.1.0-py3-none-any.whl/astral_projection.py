import subprocess
import pickle
import sys
from io import BytesIO
from base64 import b85encode, b85decode
from textwrap import dedent
from types import ModuleType
from functools import partial
from time import sleep
from collections import deque

import trio
import colorful as cf

import dont

primitive_fn = """
def is_primitive(value):
    if isinstance(value, (int, float, complex, str, bytes, type(None), type(Ellipsis))):
        return True
    elif isinstance(value, (list, tuple)):
        return all(is_primitive(element) for element in value)
    elif isinstance(value, dict):
        return all(is_primitive(item) for item in value.items())
    return False
"""
exec(primitive_fn)

def build_code(modules, variables, lines):
    result = []
    for name, module in modules.items():
        result.append(dedent(f"""
            try:
                import {module} as {name}
            except ImportError:
                pass
        """))

    payload = b85encode(pickle.dumps(variables, protocol=1)).decode()
    result.append("import pickle; import base64")
    result.append(
        f"""globals().update(
            pickle.loads(base64.b85decode('{payload}'.encode('utf-8')))
        )"""
    )
    result.extend(lines)

    result.append("print('>>%%>>')")
    result.append(primitive_fn)
    result.append("""print(
        base64.b85encode(
            pickle.dumps(
                {
                    key: value for key, value in globals().items()
                    if is_primitive(value)
                }
            )
        ).decode('utf-8')
    )
    """)

    return "\n".join(result).encode()


class host(dont):
    def __init__(self, hostname):
        self.hostname = hostname
        self.bin = "python3"

    def hook(self):
        names = {**self.frame.f_globals, **self.frame.f_locals}
        modules = {
            name: value.__name__ for name, value in names.items()
            if isinstance(value, ModuleType) and not name.startswith("__")
        }
        primitive = {
            key: value for key, value in names.items()
            if is_primitive(value) and not key.startswith("__")
        }
        code = build_code(modules, primitive, self.content)
        trio.run(self.ssh, code)

    async def ssh(self, code):
        async with trio.open_nursery() as nursery:
            process = await nursery.start(
                partial(
                    trio.run_process,
                    ["ssh", self.hostname, self.bin, "-"],
                    stdin=code,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            )
            nursery.start_soon(self.print_output, "stdout", process.stdout)
            nursery.start_soon(self.print_output, "stderr", process.stderr)

    async def print_output(self, stream_type, stream):
        if not stream:
            return
        formatter = cf.white if stream_type == "stdout" else cf.red
        payload_incoming = False
        async for data in stream:
            for line in data.rstrip(b"\n").split(b"\n"):
                if payload_incoming:
                    payload = pickle.loads(b85decode(line))
                    for key, value in payload.items():
                        exec(
                            f"{key} = {value!r}",
                            self.frame.f_globals,
                            self.frame.f_locals,
                        )
                    continue
                line = line.decode()
                if stream_type == "stdout" and line.strip() == ">>%%>>":
                    payload_incoming = True
                    continue
                print(formatter(line), file=getattr(sys, stream_type))

import errno
import fcntl
import os
import pty
import shlex
import shutil
import struct
import sys
import termios
from itertools import chain
from select import select
from subprocess import Popen
from typing import Tuple

(
    _COLUMNS,
    _ROWS,
) = shutil.get_terminal_size(fallback=(80, 20))


def _set_size(fd) -> None:  # type: ignore
    """Found at: https://stackoverflow.com/a/6420070"""
    size = struct.pack("HHHH", _ROWS, _COLUMNS, 0, 0)
    fcntl.ioctl(fd, termios.TIOCSWINSZ, size)


def run_cmd(cmd: str) -> Tuple[int, str]:
    captured_output = []
    parents, children = zip(pty.openpty(), pty.openpty())
    for fd in chain(parents, children):
        _set_size(fd)

    with Popen(
        shlex.split(cmd), stdin=sys.stdin, stdout=children[0], stderr=children[1]
    ) as p:
        for fd in children:
            os.close(fd)  # no input
        readable = {
            parents[0]: sys.stdout.buffer,  # store buffers seperately
            parents[1]: sys.stderr.buffer,
        }
        while readable:
            for fd in select(readable, [], [])[0]:
                try:
                    data = os.read(fd, 1024)  # read available
                except OSError as e:
                    if e.errno != errno.EIO:
                        raise  # XXX cleanup
                    del readable[fd]  # EIO means EOF on some systems
                else:
                    if not data:  # EOF
                        del readable[fd]
                    else:
                        if fd == parents[0]:  # We caught stdout
                            captured_output.append(data.decode("utf-8"))
                        else:
                            captured_output.append(data.decode("utf-8"))
                        readable[fd].flush()
    for fd in parents:
        os.close(fd)
    return p.returncode, "".join(captured_output)

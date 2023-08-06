import contextlib
import os
import tempfile


@contextlib.contextmanager
def temp_file(content):
    path = tempfile.mktemp()
    try:
        with open(path, "w") as f:
            f.write(content)
        yield path
    finally:
        os.unlink(path)

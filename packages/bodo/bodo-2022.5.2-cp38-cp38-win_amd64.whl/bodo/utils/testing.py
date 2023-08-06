import os
import shutil
from contextlib import contextmanager
from pathlib import Path
import bodo
cwd = Path(__file__).resolve().parent
datadir = cwd.parent / 'tests' / 'data'


@bodo.jit
def get_rank():
    return bodo.libs.distributed_api.get_rank()


@bodo.jit
def barrier():
    return bodo.libs.distributed_api.barrier()


@contextmanager
def ensure_clean(filename):
    try:
        yield
    finally:
        try:
            barrier()
            if get_rank() == 0 and os.path.exists(filename) and os.path.isfile(
                filename):
                os.remove(filename)
        except Exception as bwocb__oqmv:
            print('Exception on removing file: {error}'.format(error=
                bwocb__oqmv))


@contextmanager
def ensure_clean_dir(dirname):
    try:
        yield
    finally:
        try:
            barrier()
            if get_rank() == 0 and os.path.exists(dirname) and os.path.isdir(
                dirname):
                shutil.rmtree(dirname)
        except Exception as bwocb__oqmv:
            print('Exception on removing directory: {error}'.format(error=
                bwocb__oqmv))


@contextmanager
def ensure_clean2(pathname):
    try:
        yield
    finally:
        barrier()
        if get_rank() == 0:
            try:
                if os.path.exists(pathname) and os.path.isfile(pathname):
                    os.remove(pathname)
            except Exception as bwocb__oqmv:
                print('Exception on removing file: {error}'.format(error=
                    bwocb__oqmv))
            try:
                if os.path.exists(pathname) and os.path.isdir(pathname):
                    shutil.rmtree(pathname)
            except Exception as bwocb__oqmv:
                print('Exception on removing directory: {error}'.format(
                    error=bwocb__oqmv))

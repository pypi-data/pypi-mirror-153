import datetime as dt
import os
import pickle
import sys
import time
import traceback
from multiprocessing import Pool
from pathlib import Path
from random import choices, random
from string import printable

from killscreen.monitors import Stopwatch
import numpy as np

from dustgoggles.codex.implements import Notepad, MetaTagIndex, TagIndex, \
    GridPaper
from dustgoggles.codex.memutilz import (
    deactivate_shared_memory_resource_tracker
)

deactivate_shared_memory_resource_tracker()


def s():
    return f"{dt.datetime.now().isoformat()[-9:]},{os.getpid()}"


def log(message):
    with open("../holding/dumplog.csv", "a+") as file:
        file.write(message + "\n")


def write_garbage(
    key, size, address, delay, no_lockout, debug, notepad_type, index_type
):
    try:
        time.sleep(delay * (random() + 2) / 2)
        notes = notepad_type(
            address,
            index_type=index_type,
            no_lockout=no_lockout,
            debug=debug,
            update_on_init=False
        )
        deactivate_shared_memory_resource_tracker()
        if notepad_type == GridPaper:
            array = np.random.poisson(size=(size, size))
            notes[key] = array
        else:
            word = "".join(choices(printable, k=size))
            if index_type == MetaTagIndex:
                notes.set(key, word, len(word))
            else:
                notes[key] = word
        deactivate_shared_memory_resource_tracker()

    except Exception as exception:
        log(f"{s()},,failure: {exception};{type(exception)}")
        raise Exception("".join(traceback.format_exception(*sys.exc_info())))


def return_garbage(size, notepad_type):
    try:
        if notepad_type == GridPaper:
            value = np.random.poisson(size=(size, size))
        else:
            value = "".join(choices(printable, k=size))
        return value
    except Exception as exception:
        log(f"{s()},,failure: {exception};{type(exception)}")
        raise Exception("".join(traceback.format_exception(*sys.exc_info())))


for block in Path("/dev/shm").iterdir():
    block.unlink(missing_ok = True)
Path("../holding/dumplog.csv").unlink(missing_ok=True)

THREADS, COUNT, SIZE, DELAY = 8, 20000, 200, 0
IX_TYPE, NOTEPAD_TYPE = MetaTagIndex, GridPaper
NO_LOCKOUT, DEBUG = False, True
INDICES = choices(tuple(range(100000)), k=5000)
if __name__ == "__main__":
    notepad = NOTEPAD_TYPE(
        'codex-bounce',
        index_type=IX_TYPE,
        create=True,
        cleanup_on_exit=False,
        no_lockout=NO_LOCKOUT,
        debug=DEBUG,
        update_on_init=False
    )

    watch = Stopwatch()
    watch.start()
    results = {}
    pool = Pool(THREADS)
    settings = (
        SIZE, 'codex-bounce', DELAY, NO_LOCKOUT, DEBUG, NOTEPAD_TYPE, IX_TYPE
    )
    for ix in INDICES:
        results[ix] = pool.apply_async(write_garbage, (ix, *settings))
    pool.close()
    pool.join()
    outputs = {}
    for ix, result in results.items():
        try:
            outputs[ix] = result.get()
        except KeyboardInterrupt:
            raise
        except Exception as ex:
            outputs[ix] = ex
    exceptions = {}
    for ix, output in outputs.items():
        if isinstance(output, Exception):
            exceptions[ix] = output
    watch.click()
    with open("bounce_exceptions.pkl", "wb+") as stream:
        pickle.dump(exceptions, stream)
    print(exceptions)

    print("-------NO NOTEPAD CASE--------")
    watch = Stopwatch()
    watch.start()
    results = {}
    pool = Pool(THREADS)
    settings = (SIZE, NOTEPAD_TYPE)
    for ix in INDICES:
        results[ix] = pool.apply_async(return_garbage, settings)
    pool.close()
    pool.join()
    outputs = {}
    for ix, result in results.items():
        try:
            outputs[ix] = result.get()
        except KeyboardInterrupt:
            raise
        except Exception as ex:
            outputs[ix] = ex
    exceptions = {}
    for ix, output in outputs.items():
        if isinstance(output, Exception):
            exceptions[ix] = output
    watch.click()
    print(exceptions)

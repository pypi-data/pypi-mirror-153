import datetime as dt
import os
import pickle
import sys
import time
import traceback
from multiprocessing import Pool
from pathlib import Path
from random import choices, random, choice
from string import printable, ascii_letters

from killscreen.monitors import Stopwatch
import numpy as np

from dustgoggles.codex.implements import (
    Notepad,
    MetaTagIndex,
    TagIndex,
    GridPaper,
    FakeIndex
)
from dustgoggles.codex.memutilz import (
    deactivate_shared_memory_resource_tracker
)

# deactivate_shared_memory_resource_tracker()

with open("../dustgoggles/test_utils/data/wordlist.txt") as file:
    WORDLIST = file.readlines()

def s():
    return f"{dt.datetime.now().isoformat()[-9:]},{os.getpid()}"


def log(message):
    with open("../holding/dumplog.csv", "a+") as file:
        file.write(message + "\n")


def write_garbage(
    key, size, address, delay, no_lockout, debug, notepad_type, index_type
):
    deactivate_shared_memory_resource_tracker()
    try:
        time.sleep(delay * (random() + 2) / 2)
        notes = notepad_type(
            address,
            index_type=index_type,
            no_lockout=no_lockout,
            debug=debug,
            update_on_init=False
        )
        if notepad_type == GridPaper:
            array = np.random.poisson(size=(size, size))
            notes[key] = array
            return array
        if size == "word":
            word = choice(WORDLIST)
        else:
            word = "".join(choices(printable, k=size))
        if index_type == MetaTagIndex:
            notes.set(key, word, len(word))
        else:
            notes[key] = word
        return word
    except Exception as exception:
        log(f"{s()},,failure: {exception};{type(exception)}")
        raise Exception("".join(traceback.format_exception(*sys.exc_info())))


for block in Path("/dev/shm").iterdir():
    block.unlink(missing_ok=True)
Path("../holding/dumplog.csv").unlink(missing_ok=True)

THREADS, COUNT, SIZE, DELAY = 8, 100, 100000, 0
IX_TYPE, NOTEPAD_TYPE = TagIndex, Notepad
NO_LOCKOUT, DEBUG = False, True

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

    watch = Stopwatch(digits=3)
    watch.start()
    results = {}
    pool = Pool(THREADS)
    settings = (
        SIZE, 'codex-bounce', DELAY, NO_LOCKOUT, DEBUG, NOTEPAD_TYPE, IX_TYPE
    )
    indices = choices(tuple(range(100000)), k=COUNT)
    for ix in indices:
        results[ix] = pool.apply_async(write_garbage, (ix, *settings))
    pool.close()
    pool.join()
    outputs = {}
    stacks = {}
    for ix, result in results.items():
        try:
            outputs[ix] = result.get()
        except KeyboardInterrupt:
            raise
        except Exception as ex:
            outputs[ix] = ex
    successes, failures, exceptions = {}, {}, {}
    for ix, output in outputs.items():
        if isinstance(output, Exception):
            exceptions[ix] = output
            continue
        if isinstance(output, np.ndarray):
            successful = (notepad[ix] == output).all()
        else:
            successful = notepad[ix] == output
        if successful in (True, np.True_):
            successes[ix] = output
        else:
            failures[ix] = output
    watch.click()
    print(len(successes), len(failures), len(exceptions))
    with open("bounce_exceptions.pkl", "wb+") as stream:
        pickle.dump(exceptions, stream)
    print(exceptions)
    for ix in indices:
        try:
            del notepad[ix]
        except KeyError:
            continue
    notepad.close()

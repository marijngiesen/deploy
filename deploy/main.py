import sys
import time
from multiprocessing import Process, Queue

import debug
import daemon
import buildqueue
import registry
import repository
import queue


def run():
    processes = []

    # Create build queue
    build_queue = Queue()

    # Start buildqueue watcher
    buildqueue_watcher = Process(target=buildqueue.watch, args=(build_queue,))
    buildqueue_watcher.start()
    processes.append(buildqueue_watcher)

    # Start repository watcher
    repository_watcher = Process(target=repository.watch, args=(build_queue,))
    repository_watcher.start()
    processes.append(repository_watcher)

    # Start deploy queue watcher
    queue_watcher = Process(target=queue.watch)
    queue_watcher.start()
    processes.append(queue_watcher)

    # The main loop
    while len(processes) > 0:
        for process in processes:
            if not process.is_alive():
                process.join(2)
                processes.remove(process)

        time.sleep(1)


def main():
    foreground = False

    for arg in sys.argv:
        if "-d" in arg:
            debug.enable(registry.process)
        if "-l" in arg:
            debug.open_log(registry.process, registry.logfile)
        if "-f" in arg:
            foreground = True

    daemon.start(run, foreground)


if __name__ == "__main__":
    main()

import multiprocessing
from multiprocessing import Pool, TimeoutError
from queue import Queue
import time
from random import randint

manager = multiprocessing.Manager()
shared_queue = manager.Queue()

# Add calls to shared queue when they come in
def call_manager(call):
    try:
        shared_queue.put(call)
    except KeyboardInterrupt:
        print("Exiting Call Manager\n")

# Fetch calls from shared queue if present and print
def call_process(shared_queue):
    try:
        if not shared_queue.empty():
            call = shared_queue.get()

            # Checking behavior in scenario where one subprocess takes
            # noticeably longer than the other 3
            # time.sleep(randint(1,10))

            print(call)
    except KeyboardInterrupt:
        print("Exiting Call Processor")
        pass


# Pull values from queue so that working on
# 4 items at a time.
# When an item is added to the queue, should a flag
# be set, or should the process constantly check for
# items in the queue?
if __name__ == '__main__':

    #test_calls = [
    #"One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
    #"One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
    #"One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]

    test_calls = [
    "One", "Two", "Three"]

    for call in test_calls:
        call_manager(call)

    try:
        while True:
            if not shared_queue.empty():
                with Pool() as pool:
                    pool.map(call_process, [shared_queue,shared_queue,shared_queue,shared_queue,])
    except KeyboardInterrupt:
        print("\nClosing callManager")

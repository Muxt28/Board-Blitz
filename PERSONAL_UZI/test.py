from threading import Thread
from queue import Queue
import time

def worker(q):
    while True:
        thing = q.get()
        print(thing)
    pass    

q = Queue(maxsize=0)

thingy = Thread(target=worker, args=(q,))
thingy.start()

q.put("yo")

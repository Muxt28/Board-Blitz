from multiprocessing import pool


def hello():
    return 'Hello'

p = pool(processes=2)
p.apply_async(func=hello)

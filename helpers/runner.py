import time


def run_with_elapse(fn, *args):
    start_time = time.time()
    result = fn(*args)
    if result is not None:
        print(result)
    print("--- elapsed %s seconds ---" % (time.time() - start_time))

import time


# time scale : ns
def get_current_unixtime():
    return int(time.time() * 1000000000)

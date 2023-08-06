import time


class StopWatch:
    """
    Context manager for stopping duration of tasks.
    """

    def __init__(self, info):
        self.info = info

    def __enter__(self):
        self.tic = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        dt = time.time() - self.tic
        print(f"{self.info}: {dt:0.3f}s")

import time


class Timer:
    def __init__(self, count_max=30):
        self.latency = 1e9
        self.count = 0
        self.count_max = count_max
        self.time_previous = time.time()

    def __call__(self):
        self.count += 1
        if self.count % self.count_max == 0:
            time_now = time.time()
            self.latency = (time_now - self.time_previous) / self.count_max
            self.time_previous = time_now
        return self.latency

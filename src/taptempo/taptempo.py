import time


class TapTempo:
    """Model to tap in a tempo."""
    def __init__(self):
        self.reset()

    def tap(self):
        """Perform a single tap and calculate the bpm and averate bpm."""
        tap = time.time()
        if self.totalTaps <= 0:
            # if this is the first tap
            self.firstTap = tap
            self.lastTap = tap
        else:
            self.bpm = 60.0 / (tap - self.lastTap)
            self.bpmAvg = 60.0 / ((tap - self.firstTap) / self.totalTaps)

        self.totalTaps += 1
        self.lastTap = tap
        return self.bpm

    def reset(self):
        """Set everything to zero."""
        self.firstTap = 0
        self.lastTap = 0
        self.bpm = 0.0
        self.totalTaps = 0
        self.bpmAvg = 0.0

'''
MIT License

Copyright (c) 2020 International Business Machines

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from pyhelayers.mltoolbox.he_dl_lib.singleton import Singleton
from pyhelayers.mltoolbox.he_dl_lib.my_logger import get_logger
from time import perf_counter
logger = get_logger()
class Timer():
    def __init__(self, name):
        self.name = name
        self.counts = 0
        self.total = 0
        self.start_time = None
    def start(self):
        if self.start_time is not None:
            logger.warning(f"For Timer {self.name} start call more than once without stop - "
                           f"ignoring")
        else:
            self.start_time = perf_counter()
            self.counts += 1

    def stop(self):
        if self.start is None:
            logger.error(f"For Timer {self.name} stop was called without start - ignoring")
        else:
            self.total += perf_counter() - self.start_time
            self.start_time = None

    def report(self):
        if self.start_time is not None:
            logger.warning(f"Report called for Timer {self.name} before stopping")
            addition = perf_counter() - self.start_time
        else:
            addition = 0
        return f"total = {self.total+addition}, count = {self.counts}"

class Timers(Singleton):
    def __init__(self):
        super(Singleton).__init__()
        self.timers ={}

    def start(self, name):
        if name not in self.timers:
            self.timers[name] = Timer(name)
        self.timers[name].start()

    def stop(self, name):
        if name not in self.timers:
            logger.error(f"Stop is called on not exisitng Timer {name} - ignoring")
        else:
            self.timers[name].stop()

    def report(self):
        for timer_name, timer in self.timers.items():
            logger.log(f"Time {timer_name} - {timer.report()}")
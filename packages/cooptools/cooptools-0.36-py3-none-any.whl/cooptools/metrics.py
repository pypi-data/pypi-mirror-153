import time
from dataclasses import dataclass
from typing import List, Dict
from common import flattened_list_of_lists
from coopEnum import CoopEnum, auto

class ResultType(CoopEnum):
    SECONDS = auto()
    PERCENTAGE = auto()

@dataclass(frozen=True)
class TimeWindow:
    tags: List[str]
    start: float
    end: float

    @property
    def delta_time_s(self):
        return self.end - self.start

def time_window_factory(tw: TimeWindow,
                        start: int = None,
                        end: int = None,
                        tags: List[str] = None):
    return TimeWindow(
        tags=tags or tw.tags,
        start=start or tw.start,
        end=end or tw.end
    )
class Metrics:

    def __init__(self):
        self.time_windows: List[TimeWindow] = []
        self.start = time.perf_counter()

        #TODO: Better to refactor this so that the time info is stored by tag, not as a list of windows. Too much data

    @property
    def TotalSeconds(self):
        return time.perf_counter() - self.start

    @property
    def AllTags(self):
        return flattened_list_of_lists([x.tags for x in self.time_windows], unique=True)

    def _merge_append_timewindows(self, running_list: List[TimeWindow], new_list: List[TimeWindow]):
        if len(running_list) == 0:
            running_list = [new_list[0]]
            start = 1
        else:
            start = 0

        # merge time windows
        for ii in range(start, len(new_list)):
            if running_list[-1].tags == new_list[ii].tags:
                running_list[-1] = TimeWindow(
                    start=min(running_list[-1].start, new_list[ii].start),
                    end=max(running_list[-1].end, new_list[ii].end),
                    tags=running_list[-1].tags)
            else:
                running_list.append(new_list[ii])

        return running_list

    def add_time_windows(self, time_windows: List[TimeWindow]):
        self.time_windows = self._merge_append_timewindows(self.time_windows, time_windows)


    def windows_in_timeframe(self,
                             start=None,
                             end=None,
                             ):
        """ returns: the sum time that a tag was present between start and end"""

        windows = self.time_windows
        if start:
            splits = [time_window_factory(tw=x, start=start) for x in windows if x.start < start < x.end]
            windows = [x for x in windows if x.start > start] + splits

        if end:
            splits = [time_window_factory(tw=x, end=end) for x in windows if x.start < end < x.end]
            windows = [x for x in windows if x.end < end] + splits

        return windows


    def windows_with_tags(self,
                      start=None,
                      end=None,
                      all_tags: List[str] = None,
                      any_tags: List[str] = None):
        """ returns: the sum time that a tag was present between start and end"""

        windows_for_timeframe = self.windows_in_timeframe(start, end)

        windows_with_tag = windows_for_timeframe

        if all_tags:
            windows_with_tag = [x for x in windows_with_tag if all([y in x.tags for y in all_tags])]

        if any_tags:
            windows_with_tag = [x for x in windows_with_tag if any([y in x.tags for y in all_tags])]

        return windows_with_tag

    def s_with_tags(self,
                       start=None,
                       end=None,
                       all_tags: List[str] = None,
                       any_tags: List[str] = None
                       ):
        windows_with_tags = self.windows_with_tags(
            start=start,
            end=end,
            all_tags=all_tags,
            any_tags=any_tags
        )

        return sum([x.delta_time_s for x in windows_with_tags])

    def p_with_tags(self,
                    start=None,
                    end=None,
                    all_tags: List[str] = None,
                    any_tags: List[str] = None
                    ):
        s_with_tags = self.s_with_tags(
            start=start,
            end=end,
            all_tags=all_tags,
            any_tags=any_tags
        )

        return s_with_tags / self.TotalSeconds

    def accumulate_by_tags(self, accumResultType: ResultType, start=None, end=None) -> Dict[str, float]:
        tags = self.AllTags

        ret = {}
        for tag in tags:
            if accumResultType == ResultType.SECONDS:
                ret[tag] = self.s_with_tags(start=start, end=end, all_tags=[tag])
            elif accumResultType == ResultType.PERCENTAGE:
                ret[tag] = self.p_with_tags(start=start, end=end, all_tags=[tag])


        return ret

if __name__ == "__main__":
    import random as rnd

    m = Metrics()
    start = time.perf_counter()
    TAG = 'A'

    while True:

        time.sleep(0.1)
        end = time.perf_counter()

        tags = [TAG]
        if rnd.random() > 0.25:
            tags.append('RND')
        m.add_time_windows(time_windows=[TimeWindow(start=start, end=end, tags=tags)])
        start = end
        print(m.accumulate_by_tags(accumResultType=ResultType.PERCENTAGE), len(m.time_windows))

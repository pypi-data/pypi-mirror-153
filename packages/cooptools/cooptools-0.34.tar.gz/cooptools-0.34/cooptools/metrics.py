import time
from dataclasses import dataclass
from typing import List, Dict, Tuple
from coopEnum import CoopEnum, auto

class ResultType(CoopEnum):
    SECONDS = auto()
    PERCENTAGE = auto()

@dataclass(frozen=True)
class TimeWindow:
    start: float
    end: float

    @property
    def delta_time_s(self):
        return self.end - self.start

    def overlaps(self, other):
        if type(other) == TimeWindow:
            return self.start <= other.start <= self.end or other.start <= self.start <= other.end

    def overlap(self, other):
        if self.overlaps(other):
            return TimeWindow(
                start=max(self.start, other.start),
                end=min(self.end, other.end)
            )

        return None

    def merge(self, other):
        if not self.overlaps(other):
            raise ValueError(f"Time Windows do not overlap, so cannot merge")

        return TimeWindow(
            start=min(self.start, other.start),
            end=max(self.end, other.end)
        )


@dataclass(frozen=True)
class TaggedTimeWindow:
    window: TimeWindow
    tags: List[str]

def time_window_factory(tw: TimeWindow,
                        start: int = None,
                        end: int = None):
    return TimeWindow(
        start=start or tw.start,
        end=end or tw.end
    )

def resolve_time_window_overlap(tw1: TaggedTimeWindow, tw2: TaggedTimeWindow) -> List[TaggedTimeWindow]:
    if tw1.window == tw2.window:
        return [TaggedTimeWindow(window=tw1.window, tags=tw1.tags + tw2.tags)]

    overlap = tw1.window.overlap(tw2.window)

    # handle no overlap
    if overlap is None:
        return [tw1, tw2]

    # handle same tags
    if set(tw1.tags) == set(tw2.tags):
        return [TaggedTimeWindow(
            window=tw1.window.merge(tw2.window),
            tags=tw1.tags
        )]

    ret = []

    #1st
    if tw1.window.start < tw2.window.start:
        s1 = tw1.window.start
        e1 = tw2.window.start
        t1 = tw1.tags
    else:
        s1 = tw2.window.start
        e1 = tw1.window.start
        t1 = tw2.tags

    #2nd
    if tw2.window.start <= tw1.window.end <= tw2.window.end:
        s2 = tw2.window.start
        e2 = tw1.window.end
    elif tw1.window.start <= tw2.window.start <= tw2.window.end <= tw1.window.end:
        s2 = tw2.window.start
        e2 = tw2.window.end
    elif tw2.window.start <= tw1.window.start <= tw2.window.end:
        s2 = tw1.window.start
        e2 = tw2.window.end
    elif tw2.window.start <= tw1.window.start <= tw1.window.end <= tw2.window.end:
        s2 = tw1.window.start
        e2 = tw1.window.end
    else:
        raise NotImplementedError()

    t2 = tw1.tags + tw2.tags

    #3rd
    if tw1.window.end < tw2.window.end:
        s3 = tw1.window.end
        e3 = tw2.window.end
        t3 = tw2.tags
    else:
        s3 = tw2.window.end
        e3 = tw1.window.end
        t3 = tw1.tags

    to_add = [(s1, e1, t1),
              (s2, e2, t2),
              (s3, e3, t3)]

    for x in to_add:
        ret.append(TaggedTimeWindow(
            window=TimeWindow(
                start=x[0],
                end=x[1]
            ),
            tags=x[2]
        ))

    return ret


#
# class TimeWindowResolver:
#
#     def __init__(self):
#         self.time_windows: List[TaggedTimeWindow] = []
#
#     def add_time_window_tag(self, tagged_window: TaggedTimeWindow):
#         self.time_windows = self._merge_append_taggedtimewindows(self.time_windows, [tagged_window])
#
#     def _merge_append_taggedtimewindows(self,
#                                   running_list: List[TaggedTimeWindow],
#                                   new_list: List[TaggedTimeWindow]):
#
#         if len(running_list) == 0:
#             running_list = [new_list[0]]
#             start = 1
#         else:
#             start = 0
#
#         # merge time windows
#         for ii in range(start, len(new_list)):
#             if running_list[-1].tags == new_list[ii].tags:
#                 running_list[-1] = (TaggedTimeWindow(
#                     window=TimeWindow(
#                         start=min(running_list[-1].window.start, new_list[ii][0].start),
#                         end=max(running_list[-1][0].end, new_list[ii][0].end)
#                     )
#                     ,
#                 ), running_list[-1].tags)
#             else:
#                 running_list.append(new_list[ii])
#
#         return running_list

class Metrics:

    def __init__(self):
        self.time_windows_by_tag: Dict[str, List[TimeWindow]] = {}
        self.start = time.perf_counter()

        #TODO: Better to refactor this so that the time info is stored by tag, not as a list of windows. Too much data

    @property
    def TotalSeconds(self):
        return time.perf_counter() - self.start

    @property
    def AllTags(self):
        return list(self.time_windows_by_tag.keys())

    def tagged_windows(self, start, end) -> List[TaggedTimeWindow]:
        ret = []
        for tag, windows in self.time_windows_by_tag.items():
            windows_in_timeframe = self.windows_in_timeframe(tag, start=start, end=end)
            for window in windows_in_timeframe:
                if len(ret) == 0:
                    ret.append(TaggedTimeWindow(window, tags=[tag]))
                else:
                    new = []
                    while len(ret) > 0:
                        new += resolve_time_window_overlap(ret.pop(0), TaggedTimeWindow(window, tags=[tag]))
                    ret = new

        return ret

    def _merge_append_timewindows(self, running_list: List[TimeWindow], new_list: List[TimeWindow]):
        if len(running_list) == 0:
            running_list = [new_list[0]]
            start = 1
        else:
            start = 0

        # merge time windows
        for ii in range(start, len(new_list)):
            if running_list[-1].end >= new_list[ii].start:
                running_list[-1] = running_list[-1].merge(new_list[ii])
            else:
                running_list.append(new_list[ii])

        return running_list

    def add_time_window(self, time_window: TimeWindow, tags: List[str]):
        for tag in tags:
            self.time_windows_by_tag.setdefault(tag, [])
            self.time_windows_by_tag[tag] = self._merge_append_timewindows(self.time_windows_by_tag[tag], [time_window])

    def windows_in_timeframe(self,
                             tag: str,
                             start=None,
                             end=None,
                             ):
        """ returns: the sum time that a tag was present between start and end"""

        windows = self.time_windows_by_tag[tag]
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

        # tagged_in_window = {}
        #
        # for tag in self.AllTags:
        #     tagged_in_window[tag] = self.windows_in_timeframe(
        #         tag=tag,
        #         start=start,
        #         end=end
        #     )
        windows_with_tag = self.tagged_windows(start=start, end=end)

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

        return sum([x.window.delta_time_s for x in windows_with_tags])

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
        m.add_time_window(time_window=TimeWindow(start=start, end=end), tags=tags)
        start = end
        print(m.accumulate_by_tags(accumResultType=ResultType.PERCENTAGE), len(m.time_windows_by_tag))

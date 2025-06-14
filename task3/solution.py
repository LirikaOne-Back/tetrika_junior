from typing import Dict, List


def appearance(intervals: Dict[str, List[int]]) -> int:
    def to_segments(times: List[int]) -> List[tuple]:
        return [(times[i], times[i+1]) for i in range(0, len(times), 2)]

    lesson_start, lesson_end = intervals['lesson']
    pupil_segs = to_segments(intervals['pupil'])
    tutor_segs = to_segments(intervals['tutor'])

    def clip_and_merge(segs: List[tuple]) -> List[tuple]:
        clipped = []
        for s, e in segs:
            s_cl = max(s, lesson_start)
            e_cl = min(e, lesson_end)
            if s_cl < e_cl:
                clipped.append((s_cl, e_cl))
        if not clipped:
            return []
        clipped.sort(key=lambda x: x[0])
        merged = [clipped[0]]
        for cur_s, cur_e in clipped[1:]:
            last_s, last_e = merged[-1]
            if cur_s <= last_e:
                merged[-1] = (last_s, max(last_e, cur_e))
            else:
                merged.append((cur_s, cur_e))
        return merged

    pupil = clip_and_merge(pupil_segs)
    tutor = clip_and_merge(tutor_segs)

    total = 0
    i, j = 0, 0
    while i < len(pupil) and j < len(tutor):
        a_s, a_e = pupil[i]
        b_s, b_e = tutor[j]
        start = max(a_s, b_s)
        end   = min(a_e, b_e)
        if start < end:
            total += end - start
        if a_e < b_e:
            i += 1
        else:
            j += 1

    return total

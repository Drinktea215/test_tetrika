def appearance(intervals: dict[str, list[int]]) -> int:
    lesson_start, lesson_end = intervals['lesson']
    pupil = intervals['pupil']
    tutor = intervals['tutor']

    def get_intervals(times):
        intervals_list = []
        for i in range(0, len(times), 2):
            start = max(times[i], lesson_start)
            end = min(times[i + 1], lesson_end)
            if start < end:
                intervals_list.append((start, end))
        return intervals_list

    def merge_intervals(intervals_list):
        if not intervals_list:
            return []

        intervals_list.sort(key=lambda x: x[0])
        merged = [intervals_list[0]]
        for current in intervals_list[1:]:
            last = merged[-1]
            if current[0] <= last[1]:
                merged[-1] = (last[0], max(last[1], current[1]))
            else:
                merged.append(current)
        return merged

    pupil_intervals = merge_intervals(get_intervals(pupil))
    tutor_intervals = merge_intervals(get_intervals(tutor))

    def intersect(interval1, interval2):
        start = max(interval1[0], interval2[0])
        end = min(interval1[1], interval2[1])
        if start < end:
            return (start, end)
        else:
            return None

    total_time = 0
    i, j = 0, 0

    while i < len(pupil_intervals) and j < len(tutor_intervals):
        inter = intersect(pupil_intervals[i], tutor_intervals[j])
        if inter:
            total_time += inter[1] - inter[0]

        if pupil_intervals[i][1] < tutor_intervals[j][1]:
            i += 1
        else:
            j += 1

    return total_time


tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
                   'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                   'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
     },
    {'intervals': {'lesson': [1594702800, 1594706400],
                   'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564,
                             1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096,
                             1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500,
                             1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
                   'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3577
     },
    {'intervals': {'lesson': [1594692000, 1594695600],
                   'pupil': [1594692033, 1594696347],
                   'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565
     },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'

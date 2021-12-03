from testconfig import *

rounds = [Round('a', [["a", "b", "c", "d"], ["d'"]], []) for _ in range(3)]
rounds += [Round('a', [["a", "b", "c"], ["d", "d'"]], []) for _ in range(3)]
gst = [Round('a', [["a", "b", "c", "d", "d'"]], []) for _ in range(7)]

rounds2 = [Round('a', [["a", "b", "c"], ["d"]], []) for _ in range(3)]
rounds2 += [Round('b', [["a"], ["b", "c", "d"]], []) for _ in range(3)]
# padding for syncmanager
rounds2 += [Round('a', [["a", "b", "c", "d"]], []) for _ in range(3)]
gst2 = [Round('a', [["a", "b", "c", "d"]], []) for _ in range(7)]

test_cases = [
    TestConfig(['a','b','c','d'], ["d'"], rounds + gst, 0.8, 0, 'scenario1', 30, len(rounds), set()),
    TestConfig(['a','b','c','d'], [], rounds2 + gst2, 0.8, 0, 'scenario2', 30, len(rounds2), set()),
]

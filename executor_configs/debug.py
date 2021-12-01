from testconfig import *

test_cases = []
rounds = [Round('a', [["a", "b", "d", "d'", "c"]], []) for _ in range(2)]
rounds += [Round('a', [["a", "b", "d", "d'"], ["c"]], []) for _ in range(2)]
rounds += [Round('c', [["a", "d", "d'"], ["b", "c"]], []) for _ in range(1)]
gst = [Round('a', [["a", "b", "c", "d", "d'"]], []) for _ in range(7)]
test_cases.append(TestConfig(['a','b','c','d'], ["d'"], rounds + gst, 0.8, 0, 'test0', 30, len(rounds)))

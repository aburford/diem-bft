from testconfig import *

test_cases = []
rounds = [Round('a', [["a", "d", "d'"], ["b", "c"]], []) for _ in range(8)]
rounds += [Round('b', [["b", "d", "d'"], ["a", "c"]], []) for _ in range(8)]
rounds += [Round('c', [["c", "d", "d'"], ["b", "a"]], []) for _ in range(8)]
rounds += [Round('a', [["a", "d", "d'"], ["b", "c"]], []) for _ in range(8)]
rounds += [Round('b', [["b", "d", "d'"], ["a", "c"]], []) for _ in range(8)]
rounds += [Round('c', [["c", "d", "d'"], ["b", "a"]], []) for _ in range(8)]
gst = [Round('a', [["a", "b", "c", "d", "d'"]], []) for _ in range(7)]
test_cases.append(TestConfig(['a','b','c','d'], ["d'"], rounds + gst, 0.8, 0, 'test0', 30, len(rounds)))

from testconfig import *

test_cases = []
rounds = [Round('a', [["a", "b", "c"], ["d"], ["d'"]], []) for _ in range(2)]
rounds += [Round('a', [["a", "b", "d"], ["c"], ["d'"]], []) for _ in range(2)]
rounds += [Round('a', [["a", "c", "d"], ["b"], ["d'"]], []) for _ in range(2)]
rounds += [Round('c', [["b", "c", "d"], ["a"], ["d'"]], []) for _ in range(2)]
gst = [Round('c', [["a", "b", "c", "d", "d'"]], []) for _ in range(7)]
test_cases.append(TestConfig(['a','b','c','d'], ["d'"], rounds + gst, 0.8, 0, 'no_timeouts', 30, len(rounds), set()))

rounds = [Round('a', [["a", "b", "c"], ["d"], ["d'"]], []) for _ in range(2)]
rounds += [Round('d', [["a", "b", "d"], ["c"], ["d'"]], []) for _ in range(2)]
rounds += [Round('c', [["a", "c", "d"], ["b"], ["d'"]], []) for _ in range(2)]
rounds += [Round('b', [["b", "c", "d"], ["a"], ["d'"]], []) for _ in range(2)]
gst = [Round('c', [["a", "b", "c", "d", "d'"]], []) for _ in range(7)]
test_cases.append(TestConfig(['a','b','c','d'], ["d'"], rounds + gst, 0.8, 0, 'timeouts', 30, len(rounds), set()))

from testconfig import *

test_cases = []

#rounds = [Round('a', [["a", "b"], ["c", "d", "d'"]], []) for _ in range(1)]
#gst = [Round('a', [["a", "b", "c", "d", "d'"]], []) for _ in range(7)]
#test_cases.append(TestConfig(['a','b','c','d'], ["d'"], rounds + gst, 0.8, 0, 'without_bug', 30, len(rounds), set()))

#rounds = [Round('a', [["a", "b"], ["c", "d", "d'"]], []) for _ in range(1)]
#gst = [Round('a', [["a", "b", "c", "d", "d'"]], []) for _ in range(7)]
#test_cases.append(TestConfig(['a','b','c','d'], ["d'"], rounds + gst, 0.8, 0, 'with_bug', 30, len(rounds), {'small_quorum'}))

# TODO shouldn't property 2 be violated?
rounds = [Round('d', [["d", "a"], ["d'", "b", "c"]], []) for _ in range(3)]
gst = [Round('a', [["a", "b", "c", "d", "d'"]], []) for _ in range(7)]
test_cases.append(TestConfig(['a','b','c','d'], ["d'"], rounds + gst, 0.8, 0, 'equivocating_with_bug', 30, len(rounds), {'small_quorum'}))

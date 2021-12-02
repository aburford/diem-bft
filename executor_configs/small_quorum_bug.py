from testconfig import *

test_cases = []

rounds = [Round('a', [["a", "b"], ["c", "d", "d'"]], []) for _ in range(1)]
gst = [Round('a', [["a", "b", "c", "d", "d'"]], []) for _ in range(7)]
test_cases.append(TestConfig(['a','b','c','d'], ["d'"], rounds + gst, 0.8, 0, 'false_progress_without_bug', 30, len(rounds), set()))

rounds = [Round('a', [["a", "b"], ["c", "d", "d'"]], []) for _ in range(1)]
gst = [Round('a', [["a", "b", "c", "d", "d'"]], []) for _ in range(7)]
test_cases.append(TestConfig(['a','b','c','d'], ["d'"], rounds + gst, 0.8, 0, 'false_progress_with_bug', 30, len(rounds), {'small_quorum'}))

rounds = [Round('d', [["d", "a"], ["d'", "b", "c"]], []) for _ in range(3)]
# this round ends in timeout because a was still in round 0 so didn't know to make a proposal
rounds += [Round('a', [["a", "b", "c", "d", "d'"]], []) for _ in range(1)]
# this round ends in timeout because a hasn't received a sync response yet so it proposed a genesis block
rounds += [Round('a', [["a", "b", "c", "d", "d'"]], []) for _ in range(1)]
gst = [Round('a', [["a", "b", "c", "d", "d'"]], []) for _ in range(7)]
test_cases.append(TestConfig(['a','b','c','d'], ["d'"], rounds + gst, 0.8, 0, 'equivocating_without_bug', 30, len(rounds), set()))

rounds = [Round('d', [["d", "a"], ["d'", "b", "c"]], []) for _ in range(3)]
gst = [Round('a', [["a", "b", "c", "d", "d'"]], []) for _ in range(7)]
test_cases.append(TestConfig(['a','b','c','d'], ["d'"], rounds + gst, 0.8, 0, 'equivocating_with_bug', 60, len(rounds), {'small_quorum'}))

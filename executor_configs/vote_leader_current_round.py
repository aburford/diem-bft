from testconfig import *

rounds = [Round('a', [["a", "b", "c", "d", "d'"]], []) for _ in range(2)]
rounds += [Round('b', [["a", "b", "c", "d", "d'"]], []) for _ in range(2)]
rounds += [Round('c', [["a", "b", "c", "d", "d'"]], []) for _ in range(2)]
gst = [Round('a', [["a", "b", "c", "d", "d'"]], []) for _ in range(7)]
test_cases = [
    TestConfig(['a','b','c','d'], ["d'"], rounds + gst, 0.8, 0, 'bug', 30, 0, {'vote_leader_current_round'}),
    TestConfig(['a','b','c','d'], ["d'"], rounds + gst, 0.8, 0, 'no_bug', 30, 0, {})
]

from testconfig import *

rounds = [Round('d', [["a", "b", "c", "d", "d'"]], []) for _ in range(7)]
gst = [Round('a', [["a", "b", "c", "d", "d'"]], []) for _ in range(7)]
test_cases = [
    TestConfig(['a','b','c','d'], ["d'"], rounds + gst, 0.8, 0, 'conflicting_votes_bug', 30, len(rounds), {'conflicting_votes'}),
    TestConfig(['a','b','c','d'], ["d'"], rounds + gst, 0.8, 0, 'conflicting_votes_bug', 30, len(rounds), {})
]

from testconfig import *

gst = [Round('d', [["a", "b", "c", "d", "d'"]], []) for _ in range(7)]
test_cases = [TestConfig(['a','b','c','d'], ["d'"], gst, 0.8, 0, 'conflicting_votes_bug', 30, len(gst), {'conflicting_votes'})]

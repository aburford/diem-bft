from collections import namedtuple
from enum import Enum

# TestConfig.replicas = ['a', 'b', 'c', 'd']
# TestConfig.twins = ["d'"]
# use d and d' in the partitions
# TestConfig.rounds[0].partitions = [["a", "b", "d"], ["c", "d'"]]
TestConfig = namedtuple('TestConfig', ['replicas', 'twins', 'rounds', 'transmission_delay_bound', 'seed', 'name', 'timeout', 'gst'], defaults=(None))
Round = namedtuple('Round', ['leader', 'partition', 'exceptions'])
Except = namedtuple('Except', ['src', 'dst', 'msg_type'])
class MsgType(str,Enum):
	Proposal = 'proposal'
	TimeOut = 'timeout'
	Vote = 'vote'
	Wildcard = '*' # matches all message types

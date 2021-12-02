from collections import namedtuple
from enum import Enum

# TestConfig.replicas = ['a', 'b', 'c', 'd']
# TestConfig.twins = ["d'"]
# use d and d' in the partitions
# TestConfig.rounds[0].partitions = [["a", "b", "d"], ["c", "d'"]]
GenConfig = namedtuple('GenConfig', ['tests', 'R', 'P', 'K', 'C', 'L', 'E', 'N', 'F', 'random_partitions', 'random_leaders', 'random_configurations', 'allow_non_faulty_leaders', 'allow_quorumless_partitions', 'out_file'])
TestConfig = namedtuple('TestConfig', ['replicas', 'twins', 'rounds', 'transmission_delay_bound', 'seed', 'name', 'timeout', 'gst', 'bugs'], defaults=(None))
Round = namedtuple('Round', ['leader', 'partition', 'exceptions'])
Except = namedtuple('Except', ['src', 'dst', 'msg_type'])
class MsgType(str,Enum):
	Proposal = 'proposal'
	TimeOut = 'timeout'
	Vote = 'vote'
	Wildcard = '*' # matches all message types

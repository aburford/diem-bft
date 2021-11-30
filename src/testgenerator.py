from collections import namedtuple
from enum import Enum
import random
import json
from testconfig import *

tests = 1000
R = 1 # rounds
P = 114 # partitions
C = 1000 # round configurations
L = 4 # leader choices
E = 2 # inter partition drops

N = 7 # nodes
F = 2 # faulty nodes

random_partitions = False # random partitions
random_leaders = False # random leaders
random_configurations = False # random per-round configurations

allow_non_faulty_leaders = True

all_partitions = None
all_configurations = None

# TODO: fix partition limit and add a hook for quorumless partitions

BucketConfig = namedtuple('BucketConfig', ('bucket', 'excepts'))

# Take the first n things from the generator
def take(generator, n):
    i = 0
    for (i, thing) in enumerate(generator):
        if i >= n:
            break
        yield thing

def twin(replica):
    if '\'' in replica:
        return replica[:-1]
    else:
        return replica + '\''

originals = ['replica' + str(j) for j in range(N)]
twins = [twin(replica) for replica in take(originals, F)]
replicas = originals + twins

if allow_non_faulty_leaders:
    eligible_leaders = replicas
else:
    eligible_leaders = [replica for replica in take(originals, F)]

# Enumerates all possible intra-partition message drops
def excepts(endpoints):
    endpoints = endpoints + ['_']
    msg_types = [
        MsgType.Proposal,
        MsgType.TimeOut,
        MsgType.Vote,
        MsgType.Wildcard
    ]
    for src in endpoints:
        for dst in endpoints:
            for msg_type in msg_types:
                yield Except(src, dst, msg_type)

# Generates all samples of k things from the generator
def replacement_samples(gen, gen_args, k):
    if k == 0:
       yield []
    else:
        for sample in replacement_samples(gen, gen_args, k - 1):
            for thing in gen(*gen_args):
                yield [thing] + sample

# Generate all combinations of message drops
def except_samples(bucket):
    i = 0
    while True:
        for sample in replacement_samples(excepts, [bucket], i):
            yield sample
        i += 1

# Pick a random partition
def random_partition_gen():
    global all_partitions
    if all_partitions == None:
        all_partitions = [partition for partition in partition_gen(len(replicas))]

    while True:
        yield random.choice(all_partitions)

# Generate partitions deterministically
def partition_gen(n):
    if n == 1:
        yield [[replicas[0]]]
    else:
        # Recursively generate partitions for the n - 1 other replicas
        for partition in partition_gen(n - 1):
            for i, bucket in enumerate(partition):
                # Twins are forbidden from being in the same bucket
                if twin(replicas[n - 1]) in bucket:
                    continue
                new_partition = partition.copy()
                new_partition[i] = bucket.copy()
                new_partition[i].append(replicas[n - 1])
                yield new_partition
            partition.append([replicas[n - 1]])
            yield partition

# Randomly or deterministically generates partitions
def partitions():
    if random_partitions:
        return random_partition_gen()
    else:
        return partition_gen(len(replicas))

# Randomly or deterministically generates leaders for a bucket. "Bucket" is explained in the
# next comment
def leaders():
    if random_leaders:
        while True:
            yield random.choice(eligible_leaders)
    else:
        for leader in eligible_leaders:
            yield leader

# Generates leaders and exceptions for a set within a partition. "Set within a partition"
# is referred to as a "bucket" in the pseudocode. The authors of the Twins paper overload
# the word "partition" to refer to both the partition and the elements within it
def partition_except_sets(partition):
    if len(partition) == 0:
        yield []
    else:
        bucket = [replica for replica in partition[0]]
        for partition_except_set in partition_except_sets(partition[1:]):
            for except_sample in take(except_samples(bucket), E):
                yield except_sample + partition_except_set

# Deterministically generate the round configurations. Partitions and leaders might still
# be random if random_partitions or random_leaders is true
def round_gen():
    i = 0
    for leader in take(leaders(), L):
        for partition in take(partitions(), P):
            for partition_except_set in partition_except_sets(partition):
                i += 1
                if i >= C:
                    return
                yield Round(leader, partition, partition_except_set)

# Generates a round configuration at random. If the partitions are deterministic, it
# samples from the first P partitions. If the leaders are deterministic, it samples from
# the first L leaders
def random_round_gen():
    global all_configurations

    if all_configurations == None:
        all_configurations = [configuration for configuration in round_gen()]
    while True:
        yield random.choice(all_configurations)

# Full-partition round simulating GST (no message drops)
def GST_round():
    i = iter(replicas)
    return Round(replicas[0], [originals, twins], [])

def test_generator():
    if random_configurations:
        generator = random_round_gen
    else:
        generator = round_gen
    for test in take(replacement_samples(generator, (), R), tests):
        # Pad with seven full-parition rounds for property 4
        yield test + [GST_round()] * 7

def deserialize(test_case):
    rounds = []
    for i, rnd in enumerate(json.loads(test_case)):
        
        leader = rnd[0]
        partition = rnd[1]
        excepts = rnd[2]

        for j, ex in enumerate(excepts):
            src = ex[0]
            dst = ex[1]
            msg_type = MsgType(ex[2])
            excepts[j] = Except(src, dst, msg_type)
            
        rounds.append(Round(leader, partition, excepts))
        
    return rounds

with open('twins_tests', 'w') as out_file:
    for test in test_generator():
        test_str = json.dumps(test)
        # test_str = deserialize(test_str)
        # test_str = f'{str(test_str)}'
        out_file.write(test_str+"\n")
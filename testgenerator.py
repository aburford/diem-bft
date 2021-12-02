import os
import importlib
import random
import json
import sys
from src.testconfig import *

tests = None
R = None # rounds
P = None # partitions
K = None # buckets
C = None # round configurations
L = None # leader choices
E = None # inter partition drops

N = None # nodes
F = None # faulty nodes

random_partitions = False # random partitions
random_leaders = False # random leaders
random_configurations = False # random per-round configurations

allow_non_faulty_leaders = True
allow_quorumless_partitions = False

all_partitions = None
all_configurations = None

originals = None
twins = None
replicas = None
eligible_leaders = None

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
    return replica + '\''

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
    if all_partitions is None:
        all_partitions = list(partition_gen_quorum())

    while True:
        yield random.choice(all_partitions)

# Generate partitions deterministically
def partition_gen(n, k):
    if n == 0:
        yield []
    if k == 0 or n < k:
        return
        # Recursively generate partitions for the n - 1 other replicas
    for partition in partition_gen(n - 1, k - 1):
        partition.append([replicas[n - 1]])
        yield partition
    for partition in partition_gen(n - 1, k):
        for i, bucket in enumerate(partition):
            new_partition = partition.copy()
            new_partition[i] = bucket.copy()
            new_partition[i].append(replicas[n - 1])
            yield new_partition

def partition_gen_quorum():
    for partition in partition_gen(len(replicas), K):
        if max([len(bucket) for bucket in partition]) > 2 * F \
                or allow_quorumless_partitions:
            yield partition

# Randomly or deterministically generates partitions
def partitions():
    if random_partitions:
        return random_partition_gen()
    return partition_gen_quorum()

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
        bucket = list(partition[0])
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
    if all_configurations is None:
        all_configurations = list(round_gen())
    while True:
        yield random.choice(all_configurations)

# Full-partition round simulating GST (no message drops)
def GST_round():
    return Round(replicas[0], [originals + twins], [])

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
    for rnd in json.loads(test_case):
        leader = rnd[0]
        partition = rnd[1]
        exp = rnd[2]
        for j, ex in enumerate(exp):
            src = ex[0]
            dst = ex[1]
            msg_type = MsgType(ex[2])
            exp[j] = Except(src, dst, msg_type)
        rounds.append(Round(leader, partition, exp))
    return rounds

#pylint: disable=invalid-name,global-statement
def main():
    global tests
    global R
    global P
    global K
    global C
    global L
    global E
    global N
    global F
    global random_partitions
    global random_leaders
    global random_configurations
    global allow_non_faulty_leaders
    global allow_quorumless_partitions
    global all_partitions
    global all_configurations
    global originals
    global twins
    global replicas
    global eligible_leaders
    global originals
    global twins
    global replicas
    global eligible_leaders

    if len(sys.argv) != 2:
        print('Usage: testgenerator.py CONFIG_FILE')
        sys.exit(1)
    fname = sys.argv[1]
    config_name = os.path.basename(fname).split('.')[0]
    if fname[-3:] == '.py' or fname[-3:] == '.da':
        modname = os.path.dirname(fname).replace('/', '.') + '.' + config_name
        mod = importlib.import_module(modname)
        (tests, R, P, K, C, L, E, N, F, random_partitions, random_leaders, random_configurations, 
            allow_non_faulty_leaders, allow_quorumless_partitions, out_file) = mod.test_case
        all_partitions = None
        all_configurations = None
        originals = [chr(ord('a')+j) for j in range(N)]
        twins = [twin(replica) for replica in take(originals, F)]
        replicas = originals + twins
        if not os.path.isdir("generated_tests"):
            os.mkdir("generated_tests")
        if allow_non_faulty_leaders:
            eligible_leaders = replicas
        else:
            eligible_leaders = list(take(originals, F))
        with open("generated_tests/" + out_file, 'w') as out_file:
            json.dump(originals, out_file)
            out_file.write('\n')
            json.dump(twins, out_file)
            out_file.write('\n')
            # no bugs
            json.dump([], out_file)
            out_file.write('\n')
            for test in test_generator():
                test_str = json.dumps(test)
                # test_str = deserialize(test_str)
                # test_str = f'{str(test_str)}'
                out_file.write(test_str+"\n")
    else:
        print('we only support .py and .da configuration files')

if __name__  == '__main__':
    main()

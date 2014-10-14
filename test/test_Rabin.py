#!/usr/bin/env python

import os
from rabin import Rabin, get_file_fingerprints, set_min_block_size, set_max_block_size, set_average_block_size

TARGET = 'test.bin'
os.system("dd if=/dev/urandom of=%s bs=1024 count=100" % TARGET)


set_min_block_size(1024)
set_max_block_size(2048)
set_average_block_size(1024)

reached = []
def block_reached(start, length, fingerprint):
    # print '(%s, %s, %s)' % (start, length, fingerprint)
    reached.append((start, length, fingerprint))

r = Rabin()
r.register(block_reached)

with open(TARGET, 'r') as f:
    data = f.read()
    half = len(data) / 2
    r.update(data[:half])
    r.update(data[half:])

partial = r.fingerprints()
gold = get_file_fingerprints(TARGET)

assert len(gold) == len(partial) == len(reached)

for i in range(len(gold)):
    try:
        gs,gl,gp = gold[i]
        ps,pl,pp = partial[i]
        rs,rl,rp = reached[i]
        assert gs == ps == rs
        assert gl == pl == rl
        assert gp == pp == rp
    except:
        print 'gold   ', gold[i]
        print 'partial', partial[i]
        print 'reached', reached[i]
        raise

assert partial == gold == reached

os.unlink(TARGET)
print 'passed'

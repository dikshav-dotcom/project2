import sys
import random

# Usage: gzip -cd query.bed.gz | python3 rescale.py reference.hist query.hist > out.bed
#
# Idea: for each fragment length L we want
#     number kept at L  =  K * reference(L)
# so the kept reads have the same shape as the reference.
# We keep each read of length L with probability  K * reference(L) / query_count(L).
# K is chosen as large as possible while every "important" length (reference >= MIN_FREQ)
# still has enough query reads. Rare lengths may not have enough reads; there we keep
# all of them, so a few points can miss the reference (as the question allows).

reference_file = sys.argv[1]
query_hist_file = sys.argv[2]

MIN_FREQ = 0.001       # lengths with at least 0.1% in the reference must match
random.seed(1)         # same result every time

# Reference distribution: length -> frequency (made to add up to 1)
ref = {}
for line in open(reference_file):
    cols = line.split()
    if len(cols) >= 2:
        ref[int(cols[0])] = float(cols[1])
ref_total = sum(ref.values())
for length in ref:
    ref[length] = ref[length] / ref_total

# Query counts from query.hist (column 2): length -> number of reads
query = {}
for line in open(query_hist_file):
    cols = line.split()
    if len(cols) >= 2:
        query[int(cols[0])] = int(cols[1])

# Choose K: the smallest query_count / reference over the important lengths
K = None
for length in ref:
    if ref[length] >= MIN_FREQ:
        k = query.get(length, 0) / ref[length]
        if K is None or k < K:
            K = k

# Keep-probability for each length (never more than 1)
keep = {}
for length in query:
    p = K * ref.get(length, 0) / query[length]
    keep[length] = min(1.0, p)

# Go through the query reads and keep each one with its probability
for line in sys.stdin:
    cols = line.split()
    if len(cols) < 3:
        continue
    length = int(cols[2]) - int(cols[1])
    if random.random() < keep.get(length, 0):
        sys.stdout.write(line)

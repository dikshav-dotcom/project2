import sys

# Fragment length histogram of a BED file (read from standard input)
# Output columns: length <tab> count <tab> normalised frequency (adds up to 1)

counts = {}
total = 0

for line in sys.stdin:
    cols = line.split()
    if len(cols) < 3:
        continue
    length = int(cols[2]) - int(cols[1])      # end - start
    counts[length] = counts.get(length, 0) + 1
    total += 1

for length in sorted(counts):
    print(str(length) + "\t" + str(counts[length]) + "\t" + str(counts[length] / total))

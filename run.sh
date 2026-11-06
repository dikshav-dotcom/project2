#!/bin/bash
# Runs the whole Project 2 pipeline.
# Needs query.bed.gz and reference.hist in this folder.

# 1. Fragment length histogram of the query
gzip -cd query.bed.gz | python3 hist.py > query.hist

# 2. Sample reads from the query so its distribution matches the reference
gzip -cd query.bed.gz | python3 rescale.py reference.hist query.hist | gzip > query.rescaled.bed.gz

# 3. Histogram of the rescaled query
gzip -cd query.rescaled.bed.gz | python3 hist.py > query.rescaled.hist

# 4. Plot all three distributions
gnuplot plot.gp

echo "Reads in query:          $(gzip -cd query.bed.gz | wc -l)"
echo "Reads in rescaled query: $(gzip -cd query.rescaled.bed.gz | wc -l)"
echo "Plot: fragment_length_distributions.png"

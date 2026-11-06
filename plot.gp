# Plots the fragment length distributions: query, reference and rescaled query
set terminal pngcairo size 1000,700
set output "fragment_length_distributions.png"

set title "Fragment length distribution"
set xlabel "Fragment length (bp)"
set ylabel "Normalised frequency"
set xrange [0:700]

plot "query.hist"          using 1:3 with lines lw 2 lc rgb "purple" title "Query", \
     "reference.hist"      using 1:2 with lines lw 2 lc rgb "green"  title "Reference", \
     "query.rescaled.hist" using 1:3 with points pt 6 ps 0.6 lc rgb "#3399dd" title "Rescaled query"

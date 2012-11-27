set xlabel 'Happiness threshold'
set ylabel 'Cups per day per worker'
set terminal pdf
set output "stats.pdf"
plot './stats.tsv' w lines smooth bezier t ""

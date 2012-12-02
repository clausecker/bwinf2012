set xlabel "Glücklichkeitsschwellwert $\\alpha$"
set ylabel "Tassen pro Mitarbeiter pro Tag"
set terminal epslatex color
set output "plot.tex"
plot './stats.tsv' w lines t ""

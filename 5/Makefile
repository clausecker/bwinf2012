CFLAGS ?= -O3 -Wall

stats.pdf: stats.tsv
	gnuplot stats.gp

stats.tsv: stats
	./stats.sh

clean:
	$(RM) stats stats.tsv stats.pdf

.PHONY: clean

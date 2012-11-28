CFLAGS ?= -O3 -Wall
XELATEX ?= xelatex
GNUPLOT ?= gnuplot
PYGMENTIZE ?= pygmentize
PYGMENTIZE_STYLE ?= borland
PYGMENTIZE_OPTS ?= -O linenos

5.pdf: 5.tex stats.pdf stats.tex definitions.tex
	$(RM) *.aux
	$(XELATEX) -halt-on-error $<
	$(XELATEX) -halt-on-error $<

definitions.tex:
	$(PYGMENTIZE) -f tex -S $(PYGMENTIZE_STYLE) -f tex > $@

.c.tex:
	$(PYGMENTIZE) $(PYGMENTIZE_OPTS) -o $@ $<

stats.pdf: stats.tsv
	$(GNUPLOT) stats.gp

stats.tsv: stats
	./stats.sh

clean:
	$(RM) *.pdf *.aux *.log definitions.tex stats.tex *.tsv stats

.PHONY: clean

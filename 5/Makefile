CFLAGS ?= -O3 -Wall
XELATEX ?= xelatex
GNUPLOT ?= gnuplot
PYGMENTIZE ?= pygmentize
PYGMENTIZE_STYLE ?= borland
PYGMENTIZE_OPTS ?= -O linenos

5.pdf: 5.tex plot.tex stats.tex definitions.tex
	$(RM) *.aux
	$(XELATEX) -halt-on-error $< >/dev/null
	$(XELATEX) -halt-on-error $< >/dev/null

definitions.tex:
	$(PYGMENTIZE) -f tex -S $(PYGMENTIZE_STYLE) > $@

.c.tex:
	$(PYGMENTIZE) $(PYGMENTIZE_OPTS) -o $@ $<

plot.tex: stats.gp stats.tsv
	$(GNUPLOT) $<

stats.tsv: stats
	./stats.sh

clean:
	$(RM) *.pdf *.aux *.log definitions.tex stats.tex plot.tex *.tsv stats *.eps

.PHONY: clean

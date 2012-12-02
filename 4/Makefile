XELATEX ?= xelatex
PSTOPDF ?= pstopdf
PYTHON ?= python # python3
PYGMENTIZE ?= pygmentize
PYGMENTIZE_STYLE ?= borland
PYGMENTIZE_OPTS ?= -O linenos
RSVG_CONVERT ?= rsvg-convert
RSVG_CONVERT_OPTS ?= --height=729 --width=729
#ITERATE_OPTS ?= 

.SUFFIXES: .svg .png .py

4.pdf: 4.tex iterate.tex definitions.tex figures_all
	$(RM) *.aux
	$(XELATEX) -halt-on-error $< >/dev/null
	$(XELATEX) -halt-on-error $< >/dev/null

definitions.tex:
	$(PYGMENTIZE) -f tex -S $(PYGMENTIZE_STYLE) > $@

.svg.png:
	$(RSVG_CONVERT) $(RSVG_CONVERT_OPTS) $< > $@

.py.tex:
	$(PYGMENTIZE) $(PYGMENTIZE_OPTS) -o $@ $<

figures_all: figures_svg_all figur0.png figur0_it_1.png figur0_it_2.png figur0_it_3.png figur0_it_4.png figur0_it_5.png figur0_it_6.png

figures_svg_all: figur0_it_6.svg

figur0_it_1.svg: figur0.svg
	$(PYTHON) iterate.py $< $@

figur0_it_2.svg: figur0_it_1.svg
	$(PYTHON) iterate.py $< $@

figur0_it_3.svg: figur0_it_2.svg
	$(PYTHON) iterate.py $< $@

figur0_it_4.svg: figur0_it_3.svg
	$(PYTHON) iterate.py $< $@

figur0_it_5.svg: figur0_it_4.svg
	$(PYTHON) iterate.py $< $@

figur0_it_6.svg: figur0_it_5.svg
	$(PYTHON) iterate.py $< $@

figures_clean:
	$(RM) *.png *_it_*.svg

clean: figures_clean
	$(RM) *.pdf *.aux *.log iterate.tex definitions.tex

.PHONY: clean figures_all figures_svg_all figures_clean

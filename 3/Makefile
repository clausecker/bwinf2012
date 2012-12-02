XELATEX ?= xelatex
PSTOPDF ?= pstopdf
PYTHON ?= python # python3
PYGMENTIZE ?= pygmentize
PYGMENTIZE_STYLE ?= borland
PYGMENTIZE_OPTS ?= -O linenos
TURN90_OPTS ?= --no-interactive

.SUFFIXES: .txt .eps .pdf .py

3.pdf: 3.tex raum0_beispiel.pdf raum1.pdf raum2.pdf raum3.pdf definitions.tex turn90.tex room.tex grid_canvas.tex path.tex natives.tex
	$(RM) *.aux
	$(XELATEX) -halt-on-error $< >/dev/null
	$(XELATEX) -halt-on-error $< >/dev/null

definitions.tex:
	$(PYGMENTIZE) -f tex -S $(PYGMENTIZE_STYLE) > $@

.txt.eps: turn90.py room.py grid_canvas.py path.py natives.py
	$(PYTHON) turn90.py $(TURN90_OPTS) -o $*.eps $<

.eps.pdf:
	$(PSTOPDF) $< > /dev/null

.py.tex:
	$(PYGMENTIZE) $(PYGMENTIZE_OPTS) -o $@ $<

clean:
	$(RM) *.pdf *.aux *.log *.eps turn90.tex room.tex grid_canvas.tex path.tex definitions.tex natives.tex

.PHONY: clean

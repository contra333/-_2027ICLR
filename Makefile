MAIN := main
LATEXMK := latexmk
PYTHON ?= /home/jin/envs/research/bin/python

.PHONY: all pdf watch clean cleanall gpt-context test

all: pdf

pdf:
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error $(MAIN).tex

watch:
	$(LATEXMK) -pdf -pvc -interaction=nonstopmode -halt-on-error $(MAIN).tex

gpt-context:
	$(PYTHON) scripts/build_gpt_context.py

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py'

clean:
	$(LATEXMK) -c $(MAIN).tex

cleanall:
	$(LATEXMK) -C $(MAIN).tex

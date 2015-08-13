LATEX = xelatex

all: cabalist.pdf guru.pdf hedge_mage.pdf inspired.pdf pious.pdf primordial.pdf tech_adept.pdf voiced.pdf wayfarer.pdf

%.pdf: %.tex
	$(LATEX) $<

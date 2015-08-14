LATEX = xelatex

all: basicmoves.pdf extendedmoves.pdf cabalist.pdf guru.pdf hedge_mage.pdf inspired.pdf pious.pdf primordial.pdf tech_adept.pdf voiced.pdf wayfarer.pdf

%.pdf: %.tex playbook.tex
	$(LATEX) $<

clean:
	rm *.pdf *.aux *.log

LATEX = xelatex
PDFJOIN = pdfjoin

all: commonmoves.pdf cabalist.pdf guru.pdf hedge_mage.pdf inspired.pdf pious.pdf primordial.pdf tech_adept.pdf voiced.pdf wayfarer.pdf

%.pdf: %.tex playbook.tex
	$(LATEX) $<

basicmoves.pdf: basicmoves.tex moves.tex
	$(LATEX) basicmoves.tex

extendedmoves.pdf: extendedmoves.tex moves.tex
	$(LATEX) extendedmoves.tex

commonmoves.pdf: basicmoves.pdf extendedmoves.pdf
	$(PDFJOIN) basicmoves.pdf extendedmoves.pdf --outfile commonmoves.pdf

clean:
	rm *.pdf *.aux *.log

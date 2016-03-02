LATEX = xelatex
PDFJOIN = pdfjoin

all: commonmoves.pdf cabalist.pdf guru.pdf hedge_mage.pdf inspired.pdf pious.pdf primordial.pdf tech_adept.pdf voiced.pdf wayfarer.pdf glossary.pdf gmsheet.pdf

%.pdf: %.tex playbook.tex
	$(LATEX) $<

basicmoves.pdf: basicmoves.tex moves.tex
	$(LATEX) basicmoves.tex

extendedmoves.pdf: extendedmoves.tex moves.tex
	$(LATEX) extendedmoves.tex

commonmoves.pdf: basicmoves.pdf extendedmoves.pdf
	$(PDFJOIN) basicmoves.pdf extendedmoves.pdf --outfile commonmoves.pdf

ALL_PLAYBOOKS = cabalist.pdf guru.pdf hedge_mage.pdf inspired.pdf pious.pdf primordial.pdf tech_adept.pdf voiced.pdf wayfarer.pdf

all_playbooks.pdf: $(ALL_PLAYBOOKS)
	$(PDFJOIN) $(ALL_PLAYBOOKS) --outfile all_playbooks.pdf

clean:
	rm *.pdf *.aux *.log

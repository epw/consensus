LATEX = xelatex
PDFJOIN = pdfjoin
PANDOC = pandoc

ALL_PLAYBOOKS = cabalist.pdf mentor.pdf hedge_mage.pdf inspired.pdf pious.pdf primordial.pdf tech_adept.pdf voiced.pdf wayfarer.pdf

all: python commonmoves.pdf $(ALL_PLAYBOOKS) glossary.pdf mcsheet.pdf pcsummaries.pdf stressors.pdf living.pdf all_playbooks.pdf consensus.pdf consensus.html

python: consensus.md
	python playbookbreakout.py
	python movesbreakout.py
consensus.pdf: consensus.md
	$(PANDOC) "consensus.md" -f markdown -t latex -s -o "Consensus.pdf" --lua-filter "./pagebreak.lua" --lua-filter "./pageref.lua"

consensus.html: consensus.md
	$(PANDOC) "consensus.md" -f markdown -t html -s -o "Consensus.html" --lua-filter "./pagebreak.lua" --lua-filter "./pageref.lua"

%.pdf: %.tex playbook.tex consensus.md
	$(LATEX) $<

basicmoves.pdf: basicmoves.tex moves.tex
	$(LATEX) basicmoves.tex

extendedmoves.pdf: extendedmoves.tex moves.tex
	$(LATEX) extendedmoves.tex

commonmoves.pdf: basicmoves.pdf extendedmoves.pdf
	$(PDFJOIN) basicmoves.pdf extendedmoves.pdf --outfile commonmoves.pdf

all_playbooks.pdf: $(ALL_PLAYBOOKS)
	$(PDFJOIN) $(ALL_PLAYBOOKS) --outfile all_playbooks.pdf

clean:
	rm *.pdf *.aux *.log

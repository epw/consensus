LATEX = xelatex
PDFJOIN = pdfjoin
PANDOC = pandoc

ALL_PLAYBOOKS = cabalist.pdf hedge_mage.pdf inspired.pdf mentor.pdf pious.pdf primordial.pdf tech_adept.pdf voiced.pdf wayfarer.pdf

all: commonmoves.pdf $(ALL_PLAYBOOKS) mcsheet.pdf pcsummaries.pdf stressors.pdf all_playbooks.pdf consensus.pdf consensus.html

python: consensus.md
	python playbookbreakout.py
	python movesbreakout.py

consensus.pdf: consensus.md
	$(PANDOC) --pdf-engine=xelatex "consensus.md" -f markdown -s -o "consensus.pdf" --lua-filter "./pagebreak.lua" --lua-filter "./pageref.lua" --toc

consensus.html: consensus.md
	$(PANDOC) "consensus.md" -f markdown -t html -s -o "consensus.html" --lua-filter "./pagebreak.lua" --lua-filter "./pageref.lua"

%.pdf: %.tex playbook.tex consensus.md templates/%-template.tex
	python playbookbreakout.py $<
	$(LATEX) $<

basicmoves.pdf: basicmoves.tex moves.tex consensus.md templates/basicmoves-template.tex
	python movesbreakout.py basic
	$(LATEX) basicmoves.tex

extendedmoves.pdf: extendedmoves.tex moves.tex consensus.md templates/extendedmoves-template.tex
	python movesbreakout.py extended
	$(LATEX) extendedmoves.tex

commonmoves.pdf: basicmoves.pdf extendedmoves.pdf consensus.md
	$(PDFJOIN) basicmoves.pdf extendedmoves.pdf --outfile commonmoves.pdf

all_playbooks.pdf: $(ALL_PLAYBOOKS)
	$(PDFJOIN) $(ALL_PLAYBOOKS) --outfile all_playbooks.pdf

clean:
	rm *.pdf *.aux *.log

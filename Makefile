LATEX = xelatex
PDFJOIN = pdfjoin
PANDOC = pandoc
PYTHON = python2

ALL_PLAYBOOKS = cabalist.pdf hedge_mage.pdf inspired.pdf mentor.pdf pious.pdf primordial.pdf tech_adept.pdf voiced.pdf wayfarer.pdf

all: commonmoves.pdf $(ALL_PLAYBOOKS) mcsheet.pdf pcsummaries.pdf makingforces.pdf all_playbooks.pdf consensus.html books

books: consensus_print.pdf consensus_print_dyslexic.pdf consensus_screen.pdf consensus_screen_hc.pdf consensus_screen_dyslexic.pdf consensus_screen_dyslexic_hc.pdf

python: consensus.md
	$(PYTHON) playbookbreakout.py
	$(PYTHON) movesbreakout.py

consensus_print.pdf: consensus.md
	$(PANDOC) --pdf-engine=xelatex consensus.md print.yaml -f markdown -s -o "consensus_print.pdf" --lua-filter "./pagebreak.lua" --lua-filter "./pageref.lua" --toc --template=printtemplate --top-level-division=chapter

consensus_print_dyslexic.pdf: consensus.md
	$(PANDOC) --pdf-engine=xelatex consensus.md print_d.yaml -f markdown -s -o "consensus_print_dyslexic.pdf" --lua-filter "./pagebreak.lua" --lua-filter "./pageref.lua" --toc --template=printtemplate --top-level-division=chapter

consensus_screen.pdf: consensus.md
	$(PANDOC) --pdf-engine=xelatex consensus.md screen.yaml -f markdown -s -o "consensus_screen.pdf" --lua-filter "./pagebreak.lua" --lua-filter "./pageref.lua" --toc --template=screentemplate --top-level-division=chapter

consensus_screen_hc.pdf: consensus.md
	$(PANDOC) --pdf-engine=xelatex consensus.md screen_hc.yaml -f markdown -s -o "consensus_screen_hc.pdf" --lua-filter "./pagebreak.lua" --lua-filter "./pageref.lua" --toc --template=screentemplate --top-level-division=chapter

consensus_screen_dyslexic.pdf: consensus.md
	$(PANDOC) --pdf-engine=xelatex consensus.md screen_d.yaml -f markdown -s -o "consensus_screen_dyslexic.pdf" --lua-filter "./pagebreak.lua" --lua-filter "./pageref.lua" --toc --template=screentemplate --top-level-division=chapter

consensus_screen_dyslexic_hc.pdf: consensus.md
	$(PANDOC) --pdf-engine=xelatex consensus.md screen_d_hc.yaml -f markdown -s -o "consensus_screen_dyslexic_hc.pdf" --lua-filter "./pagebreak.lua" --lua-filter "./pageref.lua" --toc --template=screentemplate --top-level-division=chapter

consensus.html: consensus.md
	$(PANDOC) "consensus.md" -f markdown -t html -s -o "consensus.html" --lua-filter "./pagebreak.lua" --lua-filter "./pageref.lua"

%.pdf: %.tex playbook.tex consensus.md templates/%-template.tex
	$(PYTHON) playbookbreakout.py $<
	$(LATEX) $<

mcsheet.pdf: mcsheet.tex consensus.md templates/mcsheet-template.tex
	$(PYTHON) mcbreakout.py
	$(LATEX) mcsheet.tex

makingforces.pdf: makingforces.tex consensus.md templates/makingforces-template.tex
	$(PYTHON) forcesbreakout.py
	$(LATEX) makingforces.tex

basicmoves.pdf: basicmoves.tex moves.tex consensus.md templates/basicmoves-template.tex
	$(PYTHON) movesbreakout.py basic
	$(LATEX) basicmoves.tex

extendedmoves.pdf: extendedmoves.tex moves.tex consensus.md templates/extendedmoves-template.tex
	$(PYTHON) movesbreakout.py extended
	$(LATEX) extendedmoves.tex

commonmoves.pdf: basicmoves.pdf extendedmoves.pdf consensus.md
	$(PDFJOIN) basicmoves.pdf extendedmoves.pdf --outfile commonmoves.pdf

all_playbooks.pdf: $(ALL_PLAYBOOKS)
	$(PDFJOIN) $(ALL_PLAYBOOKS) --outfile all_playbooks.pdf

consensus_voices.pdf: consensus_voices.md
	$(PANDOC) --pdf-engine=xelatex consensus_voices.md screen.yaml -f markdown -s -o "consensus_voices.pdf" --lua-filter "./pagebreak.lua" --lua-filter "./pageref.lua" --toc --template=screentemplate --top-level-division=chapter

test:
	$(MAKE) -C tests test

clean:
	rm *.pdf *.aux *.log

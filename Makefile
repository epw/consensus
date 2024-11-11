LATEX = xelatex
PDFJOIN = pdfjoin
PANDOC = pandoc
PYTHON = python3

PANDOC_OPTS = -f markdown -s --lua-filter="./pagebreak.lua" --lua-filter="./pageref.lua" --from=markdown-markdown_in_html_blocks-native_divs
PANDOC_LATEX = --pdf-engine=xelatex --toc --template=screentemplate --top-level-division=chapter

ALL_PLAYBOOKS = cabalist.pdf hedge_mage.pdf inspired.pdf mentor.pdf pious.pdf primordial.pdf tech_adept.pdf voiced.pdf wayfarer.pdf

all: commonmoves.pdf $(ALL_PLAYBOOKS) mcsheet.pdf pcsummaries.pdf makingforces.pdf all_playbooks.pdf consensus.html books

books: consensus_print.pdf consensus_print_dyslexic.pdf consensus_screen.pdf consensus_screen_hc.pdf consensus_screen_dyslexic.pdf consensus_screen_dyslexic_hc.pdf

python: consensus.md
	$(PYTHON) playbookbreakout.py
	$(PYTHON) movesbreakout.py

consensus_print.pdf: consensus.md
	$(PANDOC) --pdf-engine=xelatex consensus.md print.yaml -f markdown -s -o "consensus_print.pdf" --lua-filter "./pagebreak.lua" --lua-filter "./pageref.lua" --toc --template=printtemplate --top-level-division=chapter

consensus_print_dyslexic.pdf: consensus.md
	$(PANDOC) $(PANDOC_OPTS) $(PANDOC_LATEX) consensus.md print_d.yaml -o "consensus_print_dyslexic.pdf"

consensus_screen.pdf: consensus.md
	$(PANDOC) $(PANDOC_OPTS) $(PANDOC_LATEX) consensus.md screen.yaml -o "consensus_screen.pdf"

consensus_screen_hc.pdf: consensus.md
	$(PANDOC) $(PANDOC_OPTS) $(PANDOC_LATEX) consensus.md screen_hc.yaml -o "consensus_screen_hc.pdf"

consensus_screen_dyslexic.pdf: consensus.md
	$(PANDOC) $(PANDOC_OPTS) $(PANDOC_LATEX) consensus.md screen_d.yaml -o "consensus_screen_dsylexic.pdf"

consensus_screen_dyslexic_hc.pdf: consensus.md
	$(PANDOC) $(PANDOC_OPTS) $(PANDOC_LATEX) consensus.md screen_d_hc.yaml -o "consensus_screen_dsylexic_hc.pdf"

consensus.html: consensus.md
	$(PANDOC) $(PANDOC_OPTS) "consensus.md" -t html -o "consensus.html"

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

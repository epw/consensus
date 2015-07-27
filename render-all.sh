#! /bin/bash

playbooks="cabalist.tex guru.tex hedge_mage.tex pious.tex primordial.tex tech_adept.tex"

for playbook in $playbooks
do
    xelatex $playbook
done

#! /bin/bash

playbooks="cabalist.tex guru.tex hedge_mage.tex inspired.tex pious.tex primordial.tex tech_adept.tex voiced.tex wayfarer.tex"

for playbook in $playbooks
do
    xelatex $playbook
done

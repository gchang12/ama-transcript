#!/bin/bash
cd src
if [ -e qa-contents.zip ]; then (unzip -d . qa-contents.zip; rm qa-contents.zip); fi
python3 ama_compiler.py
# Create ordered list of comments to loop over during typesetting
alias make_filename_list='mkdir "filenames"; for i in ./*/; do (ls --sort=time -r "$i" > "filenames/${i:2: -1}.txt"); done; rm filenames/filenames.txt; mv "filenames" ..'
if [ ! -e "../filenames" ]; then make_filename_list; fi
# This user's comment had to be manually edited
cp ../notes/Inazuma-sensei.txt "./Daron Nefcy/Inazuma-sensei.txt"
# Getting hyperlinks for each user
if [ ! -e "../links/" ]; then (python3 link_fetcher.py; mv links ..); fi
cd ..
# Create list of directories to loop over during typesetting
alias make_vip_list='for i in {"Daron Nefcy","Adam McArthur","Dominic Bisignano","Aaron Hammersley"}; do echo ${i/\//} >> content-creators.txt; done'
if [ ! -e content-creators.txt ]; then make_vip_list; fi
# Convert input files into TeX-friendly format
if [ ! -e "qa/" ]; then python3 parser.py; fi;
# Create emoticon files for use during typesetting
alias make_emo_files='cd emoticons; for i in ./*; do (inkscape -D -z --file=${i:2:-4}.svg --export-pdf=${i:2:-4}.pdf --export-latex); done; cd ..'
if [ ! -e "svg-inkscape" ]; then make_emo_files; fi;
# Commence typesetting
if [ ! -e ama-transcript.pdf ]; then pdflatex --shell-escape ama-transcript; fi
pdflatex ama-transcript

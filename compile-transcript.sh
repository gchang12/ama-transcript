#!/bin/bash
cd src
../_private.sh
if [ -e qa-content.tar ]; then (tar xf qa-content.tar; rm qa-content.tar); fi
python3 ama_compiler.py
# Create ordered list of comments to loop over during typesetting
if [ ! -e "../filenames" ]; then (mkdir "filenames"; for i in ./[AD]*/; do (ls --sort=time -r "$i" > "filenames/${i:2: -1}.txt"); done; mv "filenames" ..); fi
# This user's comment had to be manually edited
cp ../notes/Inazuma-sensei.txt "./Daron Nefcy/Inazuma-sensei.txt"
# Getting hyperlinks for each user
if [ ! -e "../links/" ]; then (python3 link_fetcher.py; mv links ..); fi
cd ..
# Create list of directories to loop over during typesetting
if [ ! -e content-creators.txt ]; then (for i in {"Daron Nefcy","Adam McArthur","Dominic Bisignano","Aaron Hammersley"}; do echo ${i/\//} >> content-creators.txt; done); fi
# Convert input files into TeX-friendly format
if [ ! -e "qa/" ]; then python3 parser.py; fi;
# Create emoticon files for use during typesetting
if [ ! -e "svg-inkscape" ]; then (cd emoticons; for i in ./*; do (inkscape -D -z --file=${i:2:-4}.svg --export-pdf=${i:2:-4}.pdf --export-latex); done; cd ..); fi;
# Commence typesetting
if [ ! -e ama-transcript.pdf ]; then pdflatex --shell-escape ama-transcript; fi
pdflatex ama-transcript

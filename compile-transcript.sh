#!/bin/bash
rm -fr filenames links content-creators.txt
cd src
python3 ama_compiler.py
# Create ordered list of comments to loop over during typesetting
mkdir "filenames"
for i in ./*/; do ls --sort=time -r "$i" > "filenames/${i:2: -1}.txt"; done
rm filenames/filenames.txt
mv filenames ..
# This user's comment had to be manually edited
if [ -e ../notes/Inazuma-sensei.txt ]; then mv ../notes/Inazuma-sensei.txt "./Daron Nefcy/Inazuma-sensei.txt"; fi;
# Getting hyperlinks for each user
python3 link_fetcher.py
mv links ..
cd ..
# Create list of directories to loop over during typesetting
for i in {"Daron Nefcy","Adam McArthur","Dominic Bisignano","Aaron Hammersley"}; do echo ${i/\//} >> content-creators.txt; done
# Convert input files into TeX-friendly format
python3 parser.py
# Create emoticon files for use during typesetting
cd emoticons
for i in ./*; do inkscape -D -z --file=${i:2:-4}.svg --export-pdf=${i:2:-4}.pdf --export-latex; done
cd ..
# Commence typesetting
pdflatex --shell-escape ama-transcript
pdflatex ama-transcript

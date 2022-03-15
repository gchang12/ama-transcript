#!/bin/bash
cd src
rm -fr filenames links content-creators.txt
python3 ama_compiler.py
# User must manually update this user's src file
if [ -e ../notes/Inazuma-sensei.txt ]; then read -p "Please replace './src/Daron Nefcy/Inazuma-sensei.txt' with the version in ./notes, then delete the latter. "; fi
# Sort directories into the order as it appears on the source website
touch "Daron Nefcy"
touch "Adam McArthur"
touch "Dominic Bisignano"
touch "Aaron Hammersley"
# Create list of directories to loop over during typesetting
OIFS=$IFS
IFS=$'\n'
for i in $(ls -d --sort=time -r */); do echo ${i/\//} >> content-creators.txt; done
mv -f content-creators.txt ..
IFS=$OIFS
# Create ordered list of comments to loop over during typesetting
if [ ! -e "filenames" ]; then mkdir "filenames"; fi;
for i in ./*/; do ls --sort=time -r "$i" > "filenames/${i:2: -1}.txt"; done
rm filenames/filenames.txt
mv -f filenames ..
# Getting hyperlinks for each user
python3 link_fetcher.py
mv -f links ..
cd ..
# Convert input files into TeX-friendly format
python3 parser.py
# Create emoticon files for use during typesetting
cd emoticons
for i in ./*; do inkscape -D -z --file=${i:2:-4}.svg --export-pdf=${i:2:-4}.pdf --export-latex; done
cd ..
# Commence typesetting
pdflatex --shell-escape ama-transcript
pdflatex ama-transcript

#!/bin/bash

INPUT=$1

# Replace extra commas
sed -e 's/, Del\/Dup/ Del\/Dup/g' -e 's/,DelDup Int/ DelDup Int/g' \
-e 's/, Type/ Type/g' -e 's/, DelDup/ DelDup/g' -e 's/, Fetal/ Fetal/g' \
-e 's/, Full/ Full/g' -e 's/, Int/ Int/g' -e 's/, Seq/ Seq/g' \
-e 's/, TGFBR2/ TGFBR2/g' -e 's/SDHB,C,D/SDHB_C_D/g' $INPUT > tmp

# Combine last column if accession, orderable, & varID are the same. Reformat
python /Users/331-GeeELPTP/Applications/uTOOLities/fileScripts/cut_and_paste.py tmp $1_unique.txt
rm tmp


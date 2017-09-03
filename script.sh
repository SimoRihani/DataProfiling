#!/bin/bash
read -p 'Enter 1-2 for the case of regular-unregular docs in Input/' prof
read -p 'Output name (csv) ' name
for file in `ls -a Input/*.xlsx`
  do
    echo "$file" | cut -d'.' -f1 | cut -d'/' -f2

    echo -e "\n\n\t==>\033[31m $file \033[0m\n"
    python profile_excel.py -t -u 10000 -s 0 $file > `echo "$file" | cut -d'.' -f1 | cut -d'/' -f2`".csv"
    mv `echo "$file" | cut -d'.' -f1 | cut -d'/' -f2`".csv" "stats/"
  done
for file in `ls -a stats/*.csv`
  do
    echo "$file" | cut -d'.' -f1 | cut -d'/' -f2

    echo -e "\n\n\t==>\033[31m $file \033[0m\n"
    python transform.py $file $prof > `echo "$file" | cut -d'.' -f1 | cut -d'/' -f2`"Transformed.csv"
    mv `echo "$file" | cut -d'.' -f1 | cut -d'/' -f2`"Transformed.csv" "transform/"
  done
FOO=""
for file in `ls -a transform/*.csv`
  do
    echo "$file" | cut -d'.' -f1 | cut -d'/' -f2
    FOO="$FOO $file"
    # echo -e "\n\n\t==>\033[31m $foo \033[0m\n"
  done
echo -e "\n\n\t==>\033[31m $FOO \033[0m\n"
python csv_to_excel.py $FOO
python xlsTransform.py -f `echo "output.xls"` -s 1 -r 0 -o `echo "$name.xls"`
rm `echo "output.xls"`

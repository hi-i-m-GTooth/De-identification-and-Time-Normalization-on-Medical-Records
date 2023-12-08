#!/bin/bash

cur_dir_path=$(cd "$(dirname "$0")"; pwd)

python $cur_dir_path/genaug_countries2.py
python $cur_dir_path/genaug_durations2.py # same as aug
python $cur_dir_path/genaug_orgs2.py

cat $cur_dir_path/aug2/*_answer.txt > $cur_dir_path/aug2/answer.txt
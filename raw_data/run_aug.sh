#!/bin/bash

cur_dir_path=$(cd "$(dirname "$0")"; pwd)

python $cur_dir_path/genaug_countries.py
python $cur_dir_path/genaug_durations.py
python $cur_dir_path/genaug_orgs.py

cat $cur_dir_path/aug/*_answer.txt > $cur_dir_path/aug/answer.txt
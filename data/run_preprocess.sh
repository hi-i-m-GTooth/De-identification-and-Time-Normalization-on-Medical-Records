#!/bin/bash

cur_file=$(realpath "$0")
cur_dir=$(dirname "$cur_file")

python $cur_dir/preprocess.py
#!/bin/bash

cur_file=$(realpath "$0")
cur_dir=$(dirname "$cur_file")

# train, valid
python $cur_dir/preprocess.py
# train_1prefix, valid_1prefix
python $cur_dir/preprocess.py --prefix_num 1
# train_aug
python $cur_dir/preprocess.py --aug

# test
python $cur_dir/preprocess_test.py
# test_5prefix
python $cur_dir/preprocess_test.py --prefix_num 5

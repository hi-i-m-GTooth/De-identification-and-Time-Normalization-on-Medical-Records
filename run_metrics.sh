#!/bin/bash
input=$1
label_file="raw_data/valid/answer.txt"
# check if input is empty
if [ -z $input ]; then
pred_file="submissions/DeNorm_merge/answer.txt"
else
pred_file=$input
fi

python gmetrics.py --label_file $label_file --predict_file $pred_file
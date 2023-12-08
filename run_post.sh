answer='final_submissions/empty_ans.txt'
rlt_dir='final_submissions/COUNTRY_POST'
file_dirs='raw_data/test/dataset'
# check if rlt exists, if not, create it
# if [ ! -d $rlt_dir ]; then
#     mkdir -p $rlt_dir
# fi

python gpostprocess2.py -a $answer -r $rlt_dir/answer.txt -fd $file_dirs


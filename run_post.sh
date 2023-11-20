answer='submissions/test_2ep/answer.txt'
rlt_dir='submissions/test_2ep_post'
file_dirs='raw_data/valid/dataset'
# check if rlt exists, if not, create it
if [ ! -d $rlt ]; then
    mkdir -p $rlt
fi

python gpostprocess.py -a $answer -r $rlt_dir/answer.txt -fd $file_dirs


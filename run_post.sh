answer='submissions/test_150ep/answer.txt'
rlt_dir='submissions/test_150ep_post'
file_dirs='raw_data/valid/dataset'
# check if rlt exists, if not, create it
if [ ! -d $rlt_dir ]; then
    mkdir -p $rlt_dir
fi

python gpostprocess.py -a $answer -r $rlt_dir/answer.txt -fd $file_dirs


model_dir='models/test_log_150ep/test_log_150ep_3'
rlt_dir='submissions/test_3ep'
# check if rlt exists, if not, create it
if [ ! -d $rlt_dir ]; then
    mkdir -p $rlt_dir
fi

python inference.py -md $model_dir -od $rlt_dir


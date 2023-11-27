model_dir='models/410m/410m_4'
rlt_dir='submissions/410m_4ep'
dataset_file='valid.gsv'
# check if rlt exists, if not, create it
if [ ! -d $rlt_dir ]; then
    mkdir -p $rlt_dir
fi

python inference.py -md $model_dir -od $rlt_dir -if $dataset_file


model_dir='models/410m_sche_30ep/410m_sche_30ep_3'
rlt_dir='submissions/410m_sche_30ep'
dataset_file='valid.gsv'
device='cuda:2'
batch_size=8
# check if rlt exists, if not, create it
if [ ! -d $rlt_dir ]; then
    mkdir -p $rlt_dir
fi

python inference.py -md $model_dir -od $rlt_dir -if $dataset_file -d $device -b $batch_size


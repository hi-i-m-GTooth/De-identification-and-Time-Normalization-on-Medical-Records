model_dir='models/onlyDe_410m_150ep/onlyDe_410m_150ep_4'
rlt_dir='final_submissions/onlyDe_410m_150ep_HOS'
dataset_file='test.gsv'
device='cuda:0'
batch_size=16
# check if rlt exists, if not, create it
if [ ! -d $rlt_dir ]; then
    mkdir -p $rlt_dir
fi

python inference.py -md $model_dir -od $rlt_dir -if $dataset_file -d $device -b $batch_size


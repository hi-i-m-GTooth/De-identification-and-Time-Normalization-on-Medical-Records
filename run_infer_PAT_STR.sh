model_dir='models/1prefix_410m_1'
rlt_dir='final_submissions/1prefix_410m_5prefix_PAT_STR'
dataset_file='test_5prefix.gsv'
device='cuda:0'
batch_size=64

python inference.py -md $model_dir -od $rlt_dir -if $dataset_file -d $device -b $batch_size


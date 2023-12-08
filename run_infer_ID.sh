model_dir='models/splitAll_id_410m_3'
rlt_dir='final_submissions/splitAll_ID'
dataset_file='test.gsv'
device='cuda:0'
batch_size=16

python inference.py -md $model_dir -od $rlt_dir -if $dataset_file -d $device -b $batch_size


model_dir='models/410m_4'
rlt_dir='final_submissions/410m_DEP_PHONE_LOC'
dataset_file='test.gsv'
device='cuda:0'
batch_size=16

python inference.py -md $model_dir -od $rlt_dir -if $dataset_file -d $device -b $batch_size


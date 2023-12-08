model_dir='models/160m_3'
rlt_dir='final_submissions/160m_retry3_STATE'
dataset_file='test.gsv'
device='cuda:1'
batch_size=32

python inference.py -md $model_dir -od $rlt_dir -if $dataset_file -d $device -b $batch_size


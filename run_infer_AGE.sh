model_dir='models/160m_retry5_3'
rlt_dir='final_submissions/160m_retry5_AGE'
dataset_file='test.gsv'
device='cuda:0'
batch_size=256

python inference.py -md $model_dir -od $rlt_dir -if $dataset_file -d $device -b $batch_size


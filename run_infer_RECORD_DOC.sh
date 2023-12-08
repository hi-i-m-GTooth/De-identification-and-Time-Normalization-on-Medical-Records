model_dir='models/160m_retry6_3'
rlt_dir='final_submissions/160m_retry6_RECORD_DOC'
dataset_file='test.gsv'
device='cuda:0'
batch_size=128

python inference.py -md $model_dir -od $rlt_dir -if $dataset_file -d $device -b $batch_size


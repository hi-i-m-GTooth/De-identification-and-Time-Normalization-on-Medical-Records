model_dir='models/De_410m_aug_ep20_cuda7_3'
rlt_dir='final_submissions/De_410m_aug_ep20_CITY'
dataset_file='test.gsv'
device='cuda:0'
batch_size=16

python inference.py -md $model_dir -od $rlt_dir -if $dataset_file -d $device -b $batch_size


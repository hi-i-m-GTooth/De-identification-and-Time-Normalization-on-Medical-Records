model_dir='models/Norm_410m_aug_20ep_cuda5_3'
rlt_dir='final_submissions/Norm_410m_aug_20ep_DATE_DU'
dataset_file='test.gsv'
device='cuda:0'
batch_size=32

python inference.py -md $model_dir -od $rlt_dir -if $dataset_file -d $device -b $batch_size


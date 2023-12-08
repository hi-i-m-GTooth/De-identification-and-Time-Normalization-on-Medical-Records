cur_dir_path=$(cd "$(dirname "$0")"; pwd)

epoch=150
exp_name=new_split_410m_${epoch}ep
save_epoch=1 # 0 means only save final model

# CUDA_LAUNCH_BLOCKING=1 \
python3 $cur_dir_path/../train2.py -n $exp_name --subdataset_size -1 -b 8 -e $epoch \
                            --lr 3e-5 -se $save_epoch --device cuda:0
cur_dir_path=$(cd "$(dirname "$0")"; pwd)

epoch=150
exp_name='1prefix_410m'
save_epoch=1 # 0 means only save final model

train_file=train_1prefix.gsv
valid_file=valid_1prefix.gsv

model=EleutherAI/pythia-410m
revision=step3000

python3 $cur_dir_path/../train.py -n $exp_name --subdataset_size -1 -b 4 -e $epoch \
                            --train_file $train_file --valid_file $valid_file \
                            --model_name $model --revision $revision \
                            --lr 3e-5 -se $save_epoch --device cuda:0
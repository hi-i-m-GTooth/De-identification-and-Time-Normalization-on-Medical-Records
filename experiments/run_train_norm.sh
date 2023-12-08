cur_dir_path=$(cd "$(dirname "$0")"; pwd)

epoch=30
exp_name=onlyNorm_410m_sche_30ep
save_epoch=1 # 0 means only save final model

train_file=train_norm.gsv
valid_file=valid_norm.gsv

model=EleutherAI/pythia-410m
revision=step3000

python3 $cur_dir_path/../train.py -n $exp_name --subdataset_size -1 -b 8 -e $epoch \
                            --train_file $train_file --valid_file $valid_file \
                            --model_name $model --revision $revision \
                            --lr 3e-5 -se $save_epoch --device cuda:0 \
                            --use_scheduler --use_loga16
                            
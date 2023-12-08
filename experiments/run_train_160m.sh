cur_dir_path=$(cd "$(dirname "$0")"; pwd)

epoch=10
exp_name='160m_retry9'
save_epoch=1 # 0 means only save final model

train_file=train.gsv
valid_file=valid.gsv

model=EleutherAI/pythia-160m
revision=step3000

# cuda8: b=32
python3 $cur_dir_path/../train.py -n $exp_name --subdataset_size -1 -b 32 -e $epoch \
                            --train_file $train_file --valid_file $valid_file \
                            --model_name $model --revision $revision \
                            --lr 3e-5 -se $save_epoch --device cuda:0 \
                            --use_log
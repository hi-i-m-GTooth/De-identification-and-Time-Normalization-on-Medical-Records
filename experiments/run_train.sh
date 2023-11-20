cur_dir_path=$(cd "$(dirname "$0")"; pwd)

exp_name="test_150ep"
save_epoch=0 # 0 means only save final model

python3 $cur_dir_path/../train.py -n $exp_name --subdataset_size -1 -b 8 -e 150 \
                            --lr 3e-5 --device cuda:0 \
                            -se $save_epoch
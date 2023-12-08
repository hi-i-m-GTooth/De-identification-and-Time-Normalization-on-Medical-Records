# De-identification-and-Time-Normalization-on-Medical-Records
![image](https://github.com/hi-i-m-GTooth/De-identification-and-Time-Normalization-on-Medical-Records/assets/31925572/3e4d82f0-c201-432b-a09f-b4b02176a3c7)

## Competition Page
* [Competition - CodaLab](https://codalab.lisn.upsaclay.fr/competitions/15425#participate-get_starting_kit)
* [Information Note - Hackmd](https://hackmd.io/@GTooth/ryJAkhuVa)
## 1. Raw Data Download & Rename
You'll get `first`, `second` and `valid` under `raw_data` dir.
```
bash raw_data/download.sh
```

## 2. Raw Data to Input Data / Preprocess
This script will create `train.gsv` and `valid.gsv` under `data` dir. `.gsv` is self-defined file with `{{}}` as the delimiter.  
You need to set `PREFIX_NUM` in `preprocess.py` to 0 if you don't need prefixes.
```
bash data/run_preprocess.sh
```

## 3. Train
Don't forget to set up parameters properly.
```
bash experiments/run_train.sh
```

## 4. Inference
Don't forget to set up parameters properly.
```
bash run_infer.sh
```

## 5. Post Process (Unused for Now)
Don't forget to set up parameters properly.
```
bash run_post.sh
```

## 6. Evaluate
Don't forget to set up parameters properly (you could also directly set up params through `[PATH_TO_PREDICTION_FILE]` in cmdline).  
Given your prediction `answer.txt`, this command will show you *Precision*, *Recall*, and *Macro F1* for each PHI cate.
```
bash run_metrics.sh [PATH_TO_PREDICTION_FILE]
```

# De-identification-and-Time-Normalization-on-Medical-Records
## Competition Page
* [Competition - CodaLab](https://codalab.lisn.upsaclay.fr/competitions/15425#participate-get_starting_kit)
* [Information Note - Hackmd](https://hackmd.io/@GTooth/ryJAkhuVa)
## 1. Raw Data Download & Rename
You'll get `first`, `second` and `valid` under `raw_data` dir.
```
bash raw_data/download.sh
```

## 2. Raw Data to Input Data / Preprocess
This script will create `train.gsv` and `valid.gsv` under `data` dir. `.gsv` is self-defined file with `[|||]` as the delimeter.
```
bash data/run_preprocess.sh
```

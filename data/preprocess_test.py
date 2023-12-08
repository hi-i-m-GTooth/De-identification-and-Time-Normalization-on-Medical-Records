import os
import re
from collections import defaultdict
from tqdm import tqdm
import argparse

# get current file path
cur_path = os.path.abspath(__file__)
# get current file directory
cur_dir = os.path.dirname(cur_path)
os.chdir(cur_dir)

TIMES_CATES = ["DATE", "TIME", "DURATION", "SET"]
FILE_TOKENIZERS = ['\.  ', '\n']
PREFIX_NUM = 5
raws = {
    "test": ["test"],
}

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix_num", type=int, default=0)
    args = parser.parse_args()
    return args

def write_to_gsv(data, path):
    # write csv with '\t' as delimiter
    with open(path, 'w') as f:
        for line in data:
            f.write('{{}}'.join(line) + '\n')

def read_answers(path):
    """_summary_

    Args:
        path (Path/Str): answer.txt path

    Returns:
        dict: {file_name: [{"cate":, "start":, "end":, "text":}, ...]}
    """
    rlt = defaultdict(list)
    
    with open(path, 'r') as f:
        lines = f.readlines()
    
    lines = [line.strip().split('\t') for line in lines]
    for l in lines:
        file_name, cate, start, end, text = l[0], l[1], l[2], l[3], l[4]
        text2 = l[5] if cate in TIMES_CATES else ""
        rlt[file_name].append({
            "cate": cate,
            "start": int(start),
            "end": int(end),
            "text": text,
            "text2": text2,
        })
    
    return rlt

def getBreakPoints(doc):
    break_points  = []
    for tokenizer in FILE_TOKENIZERS:
        break_points += [m.start() for m in re.finditer(tokenizer, doc)]
    break_points = sorted(break_points)
    break_points = [0] + break_points + [len(doc)]

    return break_points

def getPrefixes(text, line_indexes):
    for i in range(len(line_indexes)-1):
        line_indexes[i] = line_indexes[i+1]
    line_indexes[-1] = text.replace("\n", "")

    return line_indexes

def main(**kwargs):
    data_inline = []
    

    for dir in raws[kwargs["split"]]:
        dir_full_path = f"../raw_data/{dir}/dataset"
        files = os.listdir(dir_full_path)
        
        for file in tqdm(files):
            file_full_path = f"{dir_full_path}/{file}"
            with open(file_full_path, 'r') as f:
                doc = f.read()
            if PREFIX_NUM:
                prefixes = ["" for _ in range(PREFIX_NUM)]
                prefix = ""
            break_points = getBreakPoints(doc)

            for bp_i in range(len(break_points)-1):
                bp, bp_end = break_points[bp_i], break_points[bp_i+1]
                tmp_text = doc[bp+1:bp_end]
                tmp_text_starti = bp+1

                if tmp_text.strip() == '' or tmp_text.strip() == 'N/A' or tmp_text.strip() == 'None':
                    continue

                if PREFIX_NUM == 0:
                    data_inline.append([file.replace(".txt", ""), str(tmp_text_starti), tmp_text, "TEST: TEST"])
                else:
                    data_inline.append([file.replace(".txt", ""), str(tmp_text_starti), f"[PREFIX_START]{prefix.strip()}[PREFIX_END]{tmp_text}", "TEST: TEST"])
                
                if PREFIX_NUM:
                    prefixes = getPrefixes(tmp_text, prefixes)
                    prefix = ". ".join(filter(lambda x: x!="", prefixes))
    
    if 'aug' in raws[kwargs['split']]:
        aug = '_aug'
    elif 'aug2' in raws[kwargs['split']]:
        aug = '_aug2'
    else:
        aug = ''
    if PREFIX_NUM == 0:
        write_to_gsv(data_inline, f"./{kwargs['split']}{aug}.gsv")
    else:
        write_to_gsv(data_inline, f"./{kwargs['split']}_{PREFIX_NUM}prefix{aug}.gsv")
                    
if __name__ == "__main__":
    args = parse_args()
    PREFIX_NUM = args.prefix_num
    print("[Preprocess] test.gsv start.")
    main(split="test")
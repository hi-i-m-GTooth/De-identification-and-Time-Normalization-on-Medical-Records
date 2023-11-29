import os
import re
from collections import defaultdict
from tqdm import tqdm

# get current file path
cur_path = os.path.abspath(__file__)
# get current file directory
cur_dir = os.path.dirname(cur_path)
os.chdir(cur_dir)

TIMES_CATES = ["DATE", "TIME", "DURATION", "SET"]
FILE_TOKENIZERS = ['\.  ', '\n']
PREFIX_NUM = 0
raws = {
    "train": ["first", "second", "aug"], 
    "valid": ["valid"],
}

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
        answers = read_answers(f"../raw_data/{dir}/answer.txt")
        
        for file in tqdm(files):
            file_full_path = f"{dir_full_path}/{file}"
            with open(file_full_path, 'r') as f:
                doc = f.read()
            if PREFIX_NUM:
                prefixes = ["" for _ in range(PREFIX_NUM)]
                prefix = ""
            break_points = getBreakPoints(doc)

            answers_in_file = answers[file.replace(".txt", "")]
            ans_index = 0

            for bp_i in range(len(break_points)-1):
                bp, bp_end = break_points[bp_i], break_points[bp_i+1]
                tmp_text = doc[bp+1:bp_end]
                tmp_text_starti = bp+1

                if tmp_text.strip() == '':
                    continue
                is_got_answer, anses = False, []
                while ans_index < len(answers_in_file) and \
                    bp <= answers_in_file[ans_index]["start"] and bp_end >= answers_in_file[ans_index]["end"]:
                    anses.append(answers_in_file[ans_index])
                    ans_index += 1
                    is_got_answer = True
                if not is_got_answer:
                    if PREFIX_NUM == 0:
                        data_inline.append([file.replace(".txt", ""), str(tmp_text_starti), tmp_text, "PHI: NULL"])
                    else:
                        data_inline.append([file.replace(".txt", ""), str(tmp_text_starti), f"[PREFIX_START]{prefix.strip()}[PREFIX_END]{tmp_text}", "PHI: NULL"])
                else:
                    final_ans = []
                    for ans in anses:
                        if ans['cate'] in TIMES_CATES:
                            final_ans.append(f"{ans['cate']}: {ans['text']}=>{ans['text2']}")
                        else:
                            final_ans.append(f"{ans['cate']}: {ans['text']}")
                    if PREFIX_NUM == 0:
                        data_inline.append([file.replace(".txt", ""), str(tmp_text_starti), tmp_text, r"\n".join(final_ans)])
                    else:
                        data_inline.append([file.replace(".txt", ""), str(tmp_text_starti), f"[PREFIX_START]{prefix.strip()}[PREFIX_END]{tmp_text}", r"\n".join(final_ans)])
                if PREFIX_NUM:
                    prefixes = getPrefixes(tmp_text, prefixes)
                    prefix = ". ".join(filter(lambda x: x!="", prefixes))
    if PREFIX_NUM == 0:
        write_to_gsv(data_inline, f"./{kwargs['split']}{'_aug' if 'aug' in raws[kwargs['split']] else ''}.gsv")
    else:
        write_to_gsv(data_inline, f"./{kwargs['split']}_{PREFIX_NUM}prefix{'_aug' if 'aug' in raws[kwargs['split']] else ''}.gsv")
                    
if __name__ == "__main__":
    print("[Preprocess] train.gsv start.")
    main(split="train")
    print("[Preprocess] valid.gsv start.")
    main(split="valid")
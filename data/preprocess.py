import os
from collections import defaultdict
from tqdm import tqdm

# get current file path
cur_path = os.path.abspath(__file__)
# get current file directory
cur_dir = os.path.dirname(cur_path)
os.chdir(cur_dir)

raws = {
    "train": ["first", "second"], 
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
        rlt[file_name].append({
            "cate": cate,
            "start": int(start),
            "end": int(end),
            "text": text,
        })
    
    return rlt

def main(**kwargs):
    data_inline = []
    file_tokenizers = ['.', '\n']

    for dir in raws[kwargs["split"]]:
        dir_full_path = f"../raw_data/{dir}/dataset"
        files = os.listdir(dir_full_path)
        answers = read_answers(f"../raw_data/{dir}/answer.txt")
        
        for file in tqdm(files):
            file_full_path = f"{dir_full_path}/{file}"
            with open(file_full_path, 'r') as f:
                doc = f.read()
            
            answers_in_file = answers[file.replace(".txt", "")]
            ans_index = 0
            tmp_text, tmp_text_starti = "", 0
            for i, c in enumerate(doc):
                if c not in file_tokenizers:
                    tmp_text += c
                else:
                    tmp_text = tmp_text.strip()
                    if tmp_text:
                        if c != '\n':
                            tmp_text += c
                        is_got_answer = False
                        while ans_index < len(answers_in_file) and \
                            tmp_text_starti <= answers_in_file[ans_index]["start"] and \
                                answers_in_file[ans_index]["end"] <= i:
                            data_inline.append([file.replace(".txt", ""), str(tmp_text_starti), tmp_text, f"{answers_in_file[ans_index]['cate']}: {answers_in_file[ans_index]['text']}"])
                            ans_index += 1
                            is_got_answer = True
                        if not is_got_answer:
                            data_inline.append([file.replace(".txt", ""), str(tmp_text_starti), tmp_text, "PHI: NULL"])
                        
                    tmp_text, tmp_text_starti = "", i+1

    write_to_gsv(data_inline, f"./{kwargs['split']}.gsv")
                    
if __name__ == "__main__":
    print("[Preprocess] train.gsv start.")
    main(split="train")
    print("[Preprocess] valid.gsv start.")
    main(split="valid")
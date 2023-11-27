import argparse
import os
import re

cur_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(cur_dir)

DELIMITER = "{{}}"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", "-i", type=str, default="data/valid")

    return parser.parse_args()

def main():
    args = parse_args()
    file_name, extension = os.path.splitext(args.input_file)
    with open(args.input_file, "r") as f:
        lines = f.readlines()
    
    norm_cates = ["TIME:", "DATE:", "DURATION:", "SET:"]
    des, norms = [], []
    for line in lines:
        line = line.strip()
        ts = line.split(DELIMITER)
        text = ts[-1]
        if "PHI: NULL" in text:
            des.append(line)
            norms.append(line)
        elif any([cate in text for cate in norm_cates]):
            phis = text.split(r"\n")
            phis = list(filter(lambda x: any([cate in x for cate in norm_cates]) , phis))
            norms.append(line.replace(text, r'\n'.join(phis)))
            des.append(line.replace(text, "PHI: NULL"))
        else:
            phis = text.split(r"\n")
            phis = list(filter(lambda x: not any([cate in x for cate in norm_cates]) , phis))
            des.append(line.replace(text, r'\n'.join(phis)))
            norms.append(line.replace(text, "PHI: NULL"))
    
    with open(file_name + "_de" + extension, "w") as f:
        f.write("\n".join(des))
    with open(file_name + "_norm" + extension, "w") as f:
        f.write("\n".join(norms))

if __name__ == "__main__":
    main()
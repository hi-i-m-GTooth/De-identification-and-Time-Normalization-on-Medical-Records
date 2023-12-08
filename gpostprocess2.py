import gfunction as gf
import os
from colorama import Fore, Back, Style
import pycountry
from collections import defaultdict
from tqdm import tqdm

from parse_args import parse_args_post

current_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_path)

"""
COUNTRY POSTPROCESS
"""
def getCountries():
    rlt = []
    for country in list(pycountry.countries):
        # use common_name, official_name, name, alpha_2, alpha_3
        if hasattr(country, "common_name"):
            rlt.append(country.common_name)
        if hasattr(country, "official_name"):
            rlt.append(country.official_name)
        if hasattr(country, "name"):
            rlt.append(country.name)
        # if hasattr(country, "alpha_2"):
        #     rlt.append(country.alpha_2)
        # if hasattr(country, "alpha_3"):
        #     rlt.append(country.alpha_3)
        
    return rlt

def countryPost(file_name, file_text):
    rlt = []
    countries = getCountries()
    index = 0
    for c in countries:
        if c in ["Australia", "Mali", "Congo", "Oman", "Benin"]:
            continue
        text = file_text[index:]
        while c in text:
            country_index = text.find(c)
            rlt.append(f"{file_name}\tCOUNTRY\t{country_index}\t{country_index+len(c)}\t{c}\n")
            index += country_index+len(c)
            text = file_text[index:]
    return rlt


"""
ORGANIZATION POSTPROCESS
"""
def preprocOrgString(str):
    return str.strip().replace('\'', '').replace(',', '').lower()

def getOrgs():
    with open("./raw_data/orgs_list3.txt", "r") as f:
        orgs = f.readlines()
        orgs = [(o.strip(), preprocOrgString(o)) for o in orgs]
        for (o, prestr) in orgs:
            if '&' in o:
                o = o.replace('&', 'and')
                orgs.append((o, preprocOrgString(o)))
    return orgs

def getPreOrg2RawindexDict(file_text):
    tmp_str, dic = "", defaultdict(None)
    for i, c in enumerate(file_text):
        if c == ' ' or c == '\n':
            if tmp_str != "":
                # preString -> [(start_index, end_index)...]
                dic[preprocOrgString(tmp_str)] = [i-len(tmp_str), i-1]
                tmp_str = ""
        else:
            tmp_str += c
    if tmp_str != "":
        dic[preprocOrgString(tmp_str)] = [len(file_text)-len(tmp_str), len(file_text)-1]
    return dic

def checkPostfix(text):
    postfix = ['company', 'group', 'inc', 'corp', 'co.']
    texts = text.split(' ')
    for t in texts:
        if t == '' or t == ',' or t == '.':
            continue
        if any([p in t.lower() for p in postfix]):
            return text.find(t)+len(t.replace('.', '').replace(',', '').replace(')', '').replace('(', ''))
        break
    return -1

## Need to determine position before preprocessing
## Need to check if there is a postfix like (Company, Group, Inc)
def orgPost(file_name, file_text):
    rlt = []
    lines = gf.tokenizeString(file_text)
    for line_start_index, line in lines:
        preo2rawindex = getPreOrg2RawindexDict(line)
        # print(preo2rawindex.keys())
        for (o, pre_o) in all_orgs:
            preproc_text = preprocOrgString(line)
            
            pre_o_split = pre_o.split(' ')
            preproc_text_split = preproc_text.split(' ')
            # if all(i in preproc_text.split(' ') for i in pre_o.split(' ')):
            if pre_o_split[0] in preproc_text_split and pre_o_split[-1] in preproc_text_split:
                start_idx = preproc_text_split.index(pre_o_split[0])
                flg = True
                for idx in range(1, len(pre_o_split)):
                    if start_idx+idx >= len(preproc_text_split) or pre_o_split[idx] != preproc_text_split[start_idx+idx]:
                        flg = False
                        break
                if not flg:
                    continue

                raw_strs = o.split(' ')
                pre_o_start, pre_o_end = preprocOrgString(raw_strs[0]), preprocOrgString(raw_strs[-1])
                try:
                    org_start_index, org_end_index = preo2rawindex[pre_o_start][0], preo2rawindex[pre_o_end][1]
                except:
                    print(line)
                    print(preo2rawindex.keys())
                    print(preproc_text)
                    exit()
                if checkPostfix(line[org_end_index+1:]) != -1:
                    org_end_index += checkPostfix(line[org_end_index+1:])
                
                # no , or space at the end
                while line[org_end_index] == ',' or line[org_end_index] == ' ': 
                    org_end_index -= 1
                org_in_line = line[org_start_index:org_end_index+1]
                rlt.append(f"{file_name}\tORGANIZATION\t{line_start_index+org_start_index}\t{line_start_index+org_end_index+1}\t{org_in_line}\n")

    return rlt

def postprocess(filepath):
    file_name = filepath.split('/')[-1].split('.')[0]
    with open(filepath, 'r') as f:
        file_text = f.read()
    
    rlt = []
    rlt += countryPost(file_name, file_text)
    # rlt += orgPost(file_name, file_text)

    return rlt

def Main():
    """ Main function for postprocessing

    Args:
        kwargs (dict): arguments for postprocessing
    """
    global all_orgs
    all_orgs = getOrgs()
    args = parse_args_post()
    answer_file = args.answer_file
    result_file = args.result_file
    assert answer_file is not None, "Please specify answer file path."
    assert result_file is not None, "Please specify result file path."
    file_dirs = args.file_dir.split(',')

    rlts = []
    print(f"{Back.LIGHTYELLOW_EX}[ANS]{Style.RESET_ALL} Reading answer file ...")
    with open(answer_file, 'r') as f:
        for line in f.readlines():
            if "\tORGANIZATION\t" not in line and "\tCOUNTRY\t" not in line:
                rlts.append(line.strip()+'\n')
    print(f"{Back.LIGHTGREEN_EX}[ANS]{Style.RESET_ALL} Reading answer file finished.")
    print(f"{Back.LIGHTYELLOW_EX}[POST]{Style.RESET_ALL} Postprocessing files ...")
    for dir_path in file_dirs:
        for f in tqdm(os.listdir(dir_path)):
            if f.endswith('.txt'):
                filepath = os.path.join(dir_path, f)
                rlts += postprocess(filepath)
    print(f"{Back.LIGHTGREEN_EX}[POST]{Style.RESET_ALL} Postprocessing files finished.")
    print(f"{Back.LIGHTYELLOW_EX}[POST]{Style.RESET_ALL} Writing results ...")
    os.makedirs(os.path.dirname(result_file), exist_ok=True)
    with open(result_file, 'w') as f:
        f.writelines(rlts)
    print(f"{Back.LIGHTGREEN_EX}[POST]{Style.RESET_ALL} Writing results finished.")

if __name__ == "__main__":
    Main()
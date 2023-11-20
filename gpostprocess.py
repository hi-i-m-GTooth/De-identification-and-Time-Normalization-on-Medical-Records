import gfunction as gf
import os
from colorama import Fore, Back, Style

from parse_args import parse_args_post


current_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_path)

def postprocess(filepath):
    """ This function will postprocess the file content and get postprocessed result lines

    Args:
        filepath (string): file path of the file to be postprocessed

    Returns:
        list: postprocessed result lines
    """

    rlts = []

    lines = gf.tokenizeFile(filepath)
    for l in lines:
        file_strid, start_index, text = l[0], l[1], l[2]
        dates = gf.findAndNormalizeDates(text)
        times = gf.findAndNormalizeTimes(text)
        exist_dates = []

        # PHI: TIME
        for t in times:
            raw_t, normalized_t = t[0], t[1]
            find_idx = start_index+text.find(raw_t)
            end_find_idx = find_idx+len(raw_t)
            rlts.append(f"{file_strid}\t{'TIME'}\t{find_idx}\t{end_find_idx}\t{raw_t}\t{normalized_t}\n")
            exist_dates.append(normalized_t.split('T')[0]) # prevent duplicate in dates
        
        # PHI: DATE
        for d in dates:
            raw_d, normalized_d = d[0], d[1]
            if normalized_d not in exist_dates:
                find_idx = start_index+text.find(raw_d)
                end_find_idx = find_idx+len(raw_d)
                rlts.append(f"{file_strid}\t{'DATE'}\t{find_idx}\t{end_find_idx}\t{raw_d}\t{normalized_d}\n")

    return rlts

def Main():
    """ Main function for postprocessing

    Args:
        kwargs (dict): arguments for postprocessing
    """
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
            if "\tDATE\t" not in line and "\tTIME\t" not in line:
                rlts.append(line.strip()+'\n')
    print(f"{Back.LIGHTGREEN_EX}[ANS]{Style.RESET_ALL} Reading answer file finished.")
    print(f"{Back.LIGHTYELLOW_EX}[POST]{Style.RESET_ALL} Postprocessing files ...")
    for dir_path in file_dirs:
        for f in os.listdir(dir_path):
            if f.endswith('.txt'):
                filepath = os.path.join(dir_path, f)
                rlts += postprocess(filepath)
    print(f"{Back.LIGHTGREEN_EX}[POST]{Style.RESET_ALL} Postprocessing files finished.")
    print(f"{Back.LIGHTYELLOW_EX}[POST]{Style.RESET_ALL} Writing results ...")
    with open(result_file, 'w') as f:
        f.writelines(rlts)
    print(f"{Back.LIGHTGREEN_EX}[POST]{Style.RESET_ALL} Writing results finished.")

if __name__ == "__main__":
    Main()
        
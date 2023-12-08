import re

# file_tokenizers = ['.', '\n'] # date like 12.12.12 will be tokenized as 12 12 12
file_tokenizers = ['\n']

def tokenizeFile(filepath):
    """ This function will tokenize the file content and get tokenized result lines

    Args:
        filepath (string): file path of the file to be tokenized

    Returns:
        list of list: tokenized result lines (file_strid, start_index, text)
    """
    with open(filepath, 'r') as f:
        doc = f.read()
    
    file_strid = filepath.split('/')[-1].split('.')[0]
    tokenized_lines = []
    tmp_text, tmp_text_starti = "", 0
    for i, c in enumerate(doc):
        if c not in file_tokenizers:
            tmp_text += c
        else:
            tmp_text = tmp_text.strip()
            if tmp_text:
                if c != '\n':
                    tmp_text += c
                tokenized_lines.append([file_strid, tmp_text_starti, tmp_text])
            tmp_text, tmp_text_starti = "", i + 1
    
    return tokenized_lines

def tokenizeString(filetext):
    """ This function will tokenize the file content and get tokenized result lines

    Args:
        filepath (string): file path of the file to be tokenized

    Returns:
        list of list: tokenized result lines (start_index, text)
    """
    tokenized_lines = []
    tmp_text, tmp_text_starti = "", 0
    for i, c in enumerate(filetext):
        if c not in file_tokenizers:
            tmp_text += c
        else:
            tmp_text = tmp_text.strip()
            if tmp_text:
                if c != '\n':
                    tmp_text += c
                tokenized_lines.append([tmp_text_starti, tmp_text])
            tmp_text, tmp_text_starti = "", i + 1
    
    return tokenized_lines

def findAndNormalizeDates(input_string):
    """ Find Dates and return the list of list (original_text, normalized_text)

    Args:
        input_string (string): a line of a file

    Returns:
        list: list of list (original_text, normalized_text)
    """
    pattern1 = r'[0-9][0-9]*/[0-9][0-9]*/[0-9][0-9]*'
    pattern2 = r'[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*'
    matches = re.findall(f'({pattern1}|{pattern2})', input_string)
    if not matches:
        return []
    
    rlts = []
    for text in matches:
        if re.search(pattern1, text):
            ts = text.split('/')
            year, month, day = ts[2], int(ts[1]), int(ts[0])
        else:
            ts = text.split('.')
            year, month, day = ts[2], int(ts[1]), int(ts[0])
        
        if len(year) == 2:
            year = '20' + year
        rlts.append([text, f"{year}-{month:02}-{day:02}"])
    
    return rlts

def findAndNormalizeTimes(input_string):
    """ Find Dates+Times and return the list of list (original_text, normalized_text)

    Args:
        input_string (string): a line of a file

    Returns:
        list: list of list (original_text, normalized_text)
    """
    pattern1_24 = r'[0-9][0-9]*[:\.][0-9][0-9]* on [0-9][0-9]*/[0-9][0-9]*/[0-9][0-9]*'
    pattern2_24 = r'[0-9][0-9]*[:\.][0-9][0-9]* on [0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*'
    pattern1_12 = r'[0-9][0-9]*[:\.][0-9][0-9]*[ap]m on [0-9][0-9]*/[0-9][0-9]*/[0-9][0-9]*'
    pattern2_12 = r'[0-9][0-9]*[:\.][0-9][0-9]*[ap]m on [0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*'
    pattern1_24_at = r'[0-9][0-9]*/[0-9][0-9]*/[0-9][0-9]* at [0-9][0-9]*[:\.][0-9][0-9]*'
    pattern2_24_at = r'[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]* at [0-9][0-9]*[:\.][0-9][0-9]*'
    pattern1_12_at = r'[0-9][0-9]*/[0-9][0-9]*/[0-9][0-9]* at [0-9][0-9]*[:\.][0-9][0-9]*[ap]m'
    pattern2_12_at = r'[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]* at [0-9][0-9]*[:\.][0-9][0-9]*[ap]m'
    matches = re.findall(f'({pattern1_24}|{pattern2_24}|{pattern1_12}|{pattern2_12}|{pattern1_24_at}|{pattern2_24_at}|{pattern1_12_at}|{pattern2_12_at})', input_string)
    if not matches:
        return []
    
    rlts = []
    for text in matches:
        if re.search(pattern1_24, text) or re.search(pattern2_24, text):
            ts = list(map(lambda x: x.strip(), text.split('on')))
            date = re.split('\.|/', ts[1])
            year, month, day = date[2], int(date[1]), int(date[0])
            time = re.split(':|\.', ts[0])
            hour, minute = int(time[0]), int(time[1])
        elif re.search(pattern1_12, text) or re.search(pattern2_12, text):
            ts = list(map(lambda x: x.strip(), text.split('on')))
            pm = False if 'am' in ts[0] else True
            date = re.split('\.|/', ts[1])
            year, month, day = date[2], int(date[1]), int(date[0])
            time = re.split(':|\.', ts[0].replace('am', '').replace('pm', '').strip())
            hour, minute = int(time[0]) + 12 if pm else int(time[0]), int(time[1])
        elif re.search(pattern1_24_at, text) or re.search(pattern2_24_at, text):
            ts = list(map(lambda x: x.strip(), text.split('at')))
            date = re.split('\.|/', ts[0])
            year, month, day = date[2], int(date[1]), int(date[0])
            time = re.split(':|\.', ts[1])
            hour, minute = int(time[0]), int(time[1])
        else:
            ts = list(map(lambda x: x.strip(), text.split('at')))
            pm = False if 'am' in ts[1] else True
            date = re.split('\.|/', ts[0])
            year, month, day = date[2], int(date[1]), int(date[0])
            time = re.split(':|\.', ts[1].replace('am', '').replace('pm', '').strip())
            hour, minute = int(time[0]) + 12 if pm else int(time[0]), int(time[1])

        if len(year) == 2:
            year = '20' + year
        rlts.append([text, f"{year}-{month:02}-{day:02}T{hour:02}:{minute:02}"])

    return rlts

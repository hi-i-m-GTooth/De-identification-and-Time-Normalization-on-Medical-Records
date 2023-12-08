import os
import random

cur_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(cur_dir)
# str:int = 1:10
str_nums = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
str_num_dict = {str_nums[i]: i+1 for i in range(len(str_nums))}
i_nums = list(range(1, 20+1)) + list(range(1, 20+1)) + list(range(1, 20+1)) + list(range(21, 100+1))
i_nums_dict = {i: i for i in range(1, 100+1)}
nums_dict = {**str_num_dict, **i_nums_dict}

_uniq_times = ["hours", "days", "weeks", "months", "years", "yrs", "wks", "hrs", "hour", "day", "week", "month", "year", "yr", "wk", "hr"]
times = ["hours", "days", "weeks", "months", "years", "yrs", "wks", "hrs"]*56 + ["hour", "day", "week", "month", "year", "yr", "wk", "hr"]*10
times_norm_dict = {_uniq_times[i]: (_uniq_times[i][0]).upper() for i in range(len(_uniq_times))}

delimiters = ['' for _ in range(29)] + [' ' for _ in range(66)] + ['/' for _ in range(5)]

def getDuNorm():
    str_num = random.choice(str_nums)
    i_num = random.choice(i_nums)
    num = random.choice([str_num]+ [i_num for _ in range(12)])
    delimiter = random.choice(delimiters)
    time = random.choice(times)
    if nums_dict[num] == 1 and time.endswith('s'):
        time = time[:-1]
        
    norm_num = nums_dict[num]
    norm_time = times_norm_dict[time]

    du = f"{num}{delimiter}{time}"
    norm = f"P{norm_num}{norm_time}"
    return du, norm


def getTextAnsDuTrips():
    results = []
    with open("./duration_trains.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            ts = line.strip().split("{{}}")
            if len(ts) < 4:
                continue
            text = ts[2]
            du, ans = "", []
            for a in ts[-1].split(r'\n'):
                if a.startswith("DURATION:"):
                    du = a.split(": ")[1]
                    du = du.split("=>")[0]
                else:
                    ans.append(a.split(": "))
            results.append({"text": text, "answers": ans, "du": du})

    return results


def main():
    data_f = open("./aug2/dataset/dus.txt", "w")
    ans_f = open("./aug2/du_answer.txt", "w")
    data_fpointer = 0

    trips = getTextAnsDuTrips()
    for _ in range(5000):
        trip = random.choice(trips)
        du, norm = getDuNorm()
        old_du = trip["du"]
        text = trip["text"].replace(old_du, du) + "\n"
        data_f.write(text)
        for ans in trip["answers"]:
            cate, content = ans
            start = text.find(content)
            end = start + len(content) - 1
            if "=>" in content:
                content, content2 = content.split("=>")
                content = f"{content}\t{content2}"
            ans_f.write(f"dus\t{cate}\t{data_fpointer+start}\t{data_fpointer+end}\t{content}\n")
        start = text.find(du)
        end = start + len(du) - 1
        ans_f.write(f"dus\tDURATION\t{data_fpointer+start}\t{data_fpointer+end}\t{du}\t{norm}\n")
        data_fpointer += len(text)
    
    data_f.close()
    ans_f.close()

if __name__ == "__main__":
    main()



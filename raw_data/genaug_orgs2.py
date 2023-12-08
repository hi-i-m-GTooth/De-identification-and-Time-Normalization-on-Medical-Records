import os
import random

cur_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(cur_dir)

def getTextAnsOrgTrips():
    results = []
    with open("./org_trains.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            ts = line.strip().split("{{}}")
            if len(ts) < 4:
                continue
            text = ts[2]
            org, ans = "", []
            for a in ts[-1].split(r'\n'):
                if a.startswith("ORGANIZATION:"):
                    org = a.split(": ")[1]
                else:
                    ans.append(a.split(": "))
            results.append({"text": text, "answers": ans, "org": org})

    return results

def getOrgs():
    orgs = []
    with open("./orgs_list.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            orgs.append(line.strip())
    return orgs


def main():
    data_f = open("./aug2/dataset/orgs.txt", "w")
    ans_f = open("./aug2/org_answer.txt", "w")
    data_fpointer = 0

    orgs = getOrgs()
    for _ in range(5):
        for org in orgs:
            text = org + "\n"
            data_f.write(text)
            start = 0
            end = start + len(org) - 1
            ans_f.write(f"orgs\tORGANIZATION\t{data_fpointer+start}\t{data_fpointer+end}\t{org}\n")
            data_fpointer += len(text)
    
    data_f.close()
    ans_f.close()

if __name__ == "__main__":
    main()



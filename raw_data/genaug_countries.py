import os
import pycountry
import random

cur_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(cur_dir)

FORMAT_ANS_PAIRS = [
                        {"format": "  If the family history is suggestive, ursodeoxycholic acid is of benefit to prevent lithiasis. I am not aware of any {country} centres that provided MDR3 gene analysis",
                        "answers": []
                        },
                        {"format": "[Low grade myoepithelial carcinoma with positivemargins reviewed by Dr Moses CUJAS, WESTON {country}].",
                        "answers": ["DOCTOR: Moses CUJAS", "CITY: WESTON"]
                        }, 
                        {"format": "The tumour appears to fit the description of the tumour in the initial resection (diagnosed as amyoepithelial carcinoma, low grade by Dr Flynn Bredahl in GOONDIWINDI, {country}).",
                        "answers": ["DOCTOR: Flynn Bredahl", "CITY: GOONDIWINDI"]
                        }
                    ]


def getCountries():
    rlt = []
    for country in list(pycountry.countries):
        if hasattr(country, "common_name"):
            rlt.append(country.common_name)
        if hasattr(country, "official_name"):
            rlt.append(country.official_name)
        if hasattr(country, "name"):
            rlt.append(country.name)
        if hasattr(country, "alpha_2"):
            rlt.append(country.alpha_2)
        if hasattr(country, "alpha_3"):
            rlt.append(country.alpha_3)
    return rlt

def main():
    data_f = open("./aug/dataset/countries.txt", "w")
    ans_f = open("./aug/country_answer.txt", "w")
    data_fpointer = 0

    countries = getCountries()
    for pair in FORMAT_ANS_PAIRS:
        for country in countries:
            text = pair["format"].format(country=country) + "\n"
            data_f.write(text)
            for ans in pair["answers"]:
                ts = list(map(lambda x: x.strip(), ans.split(": ")))
                start = text.find(ts[1])
                end = start + len(ts[1]) - 1
                ans_f.write(f"countries\t{ts[0]}\t{data_fpointer+start}\t{data_fpointer+end}\t{ts[1]}\n")
            start = text.find(country)
            end = start + len(country) - 1
            ans_f.write(f"countries\tCOUNTRY\t{data_fpointer+start}\t{data_fpointer+end}\t{country}\n")
            data_fpointer += len(text)
    
    data_f.close()
    ans_f.close()

if __name__ == "__main__":
    main()



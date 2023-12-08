import os
import pycountry
import random

cur_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(cur_dir)

def getCountries():
    rlt = []
    for country in list(pycountry.countries):
        if hasattr(country, "common_name"):
            rlt.append(country.common_name)
        if hasattr(country, "official_name"):
            rlt.append(country.official_name)
        if hasattr(country, "name"):
            rlt.append(country.name)
    return rlt

def main():
    data_f = open("./aug2/dataset/countries.txt", "w")
    ans_f = open("./aug2/country_answer.txt", "w")
    data_fpointer = 0

    countries = getCountries()
    print("# Countries:", len(countries))
    for _ in range(5):
        for country in countries:
            text = country + "\n"
            data_f.write(text)
            start = 0
            end = start + len(country) - 1
            ans_f.write(f"countries\tCOUNTRY\t{data_fpointer+start}\t{data_fpointer+end}\t{country}\n")
            data_fpointer += len(text)
    
    data_f.close()
    ans_f.close()

if __name__ == "__main__":
    main()



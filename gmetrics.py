import os

cur_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(cur_dir)

from parse_args import parse_args_metrics
from collections import defaultdict
from colorama import Fore, Back, Style

class Metrics:
    def __init__(self, label_file, predict_file) -> None:
        self.label_file = label_file
        self.predict_file = predict_file
        self.label_sets, self.predict_sets = self.getSets(self.label_file), self.getSets(self.predict_file)
    
    def getSets(self, file):
        sets = {"de": defaultdict(set), "norm": defaultdict(set)}
        with open(file, 'r', encoding='utf8') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line == '':
                    continue
                
                ts = line.split('\t')
                if len(ts) == 5:
                    sets["de"][ts[1]].add(line)
                elif len(ts) == 6:
                    sets["de"][ts[1]].add(line)
                    sets["norm"][ts[1]].add(line)
                else:
                    continue

        return sets

class Precision(Metrics):
    def __init__(self, label_file, predict_file) -> None:
        super().__init__(label_file, predict_file)
    
    def calculate(self):
        """Calculate the precision of each PHI type.

        Returns:
            de_precisions (dict): Precision of each de-identification PHI type.
            norm_precisions (dict): Precision of each normalization PHI type.
        """
        de_precisions, norm_precisions = {}, {}
        for key in self.label_sets["de"]:
            de_precisions[key] = len(self.label_sets["de"][key].intersection(self.predict_sets["de"][key])) / (len(self.predict_sets["de"][key])+1e-7)
        for key in self.label_sets["norm"]:
            norm_precisions[key] = len(self.label_sets["norm"][key].intersection(self.predict_sets["norm"][key])) / (len(self.predict_sets["norm"][key])+1e-7)
        return de_precisions, norm_precisions

class Recall(Metrics):
    def __init__(self, label_file, predict_file) -> None:
        super().__init__(label_file, predict_file)
    
    def calculate(self):
        """Calculate the recall of each PHI type.

        Returns:
            de_recalls (dict): Recall of each de-identification PHI type.
            norm_recalls (dict): Recall of each normalization PHI type.
        """
        de_recalls, norm_recalls = {}, {}
        for key in self.label_sets["de"]:
            de_recalls[key] = len(self.label_sets["de"][key].intersection(self.predict_sets["de"][key])) / (len(self.label_sets["de"][key]))+1e-7
        for key in self.label_sets["norm"]:
            norm_recalls[key] = len(self.label_sets["norm"][key].intersection(self.predict_sets["norm"][key])) / len(self.label_sets["norm"][key])+1e-7
        return de_recalls, norm_recalls
    
class MacroF1Score:
    def __init__(self, precision, recall) -> None:
        self.precision = precision
        self.recall = recall
    
    def calculate(self):
        """Calculate the F1 macro score of each PHI type.

        Returns:
            de_f1s (dict): F1 macro score of each de-identification PHI type.
            norm_f1s (dict): F1 macro score of each normalization PHI type.
        """
        de_precisions, norm_precisions = self.precision.calculate()
        de_recalls, norm_recalls = self.recall.calculate()
        de_f1s, norm_f1s = {}, {}
        for key in de_precisions:
            de_f1s[key] = 2 * de_precisions[key] * de_recalls[key] / (de_precisions[key] + de_recalls[key] + 1e-7)
        for key in norm_precisions:
            norm_f1s[key] = 2 * norm_precisions[key] * norm_recalls[key] / (norm_precisions[key] + norm_recalls[key]+ 1e-7)
        return de_f1s, norm_f1s

def main():
    args = parse_args_metrics()
    precision = Precision(args.label_file, args.predict_file)
    recall = Recall(args.label_file, args.predict_file)
    de_macro_f1_score, norm_macro_f1_score = MacroF1Score(precision, recall).calculate()
    de_precisions, norm_precisions = precision.calculate()
    de_recalls, norm_recalls = recall.calculate()
    # DE
    DE_TYPE = precision.label_sets["de"].keys()
    print(f"{'PHITYPE':<20} {'Precision':<20} {'Recall':<20} {'F1-Macro':<20} {'Support':<20}")
    print("=======================================================================================")
    for key in DE_TYPE:
        print(f"{key:<20} {de_precisions[key]:<20.4f} {de_recalls[key]:<20.4f} {de_macro_f1_score[key]:<20.4f} {len(precision.label_sets['de'][key]):<20}")
    print("=======================================================================================")
    print(f"{'Macro-Average':<20} {sum(de_precisions.values())/len(de_precisions):<20.4f} {sum(de_recalls.values())/len(de_recalls):<20.4f} {sum(de_macro_f1_score.values())/len(de_macro_f1_score):<20.4f} {sum([len(s) for s in precision.label_sets['de'].values()]):<20}")

    print("\n")

    # NORM
    NORM_TYPE = precision.label_sets["norm"].keys()
    print(f"{'PHITYPE':<20} {'Precision':<20} {'Recall':<20} {'F1-Macro':<20} {'Support':<20}")
    print("=======================================================================================")
    for key in NORM_TYPE:
        print(f"{key:<20} {norm_precisions[key]:<20.4f} {norm_recalls[key]:<20.4f} {norm_macro_f1_score[key]:<20.4f} {len(precision.label_sets['norm'][key]):<20}")
    print("=======================================================================================")
    print(f"{'Macro-Average':<20} {sum(norm_precisions.values())/len(norm_precisions):<20.4f} {sum(norm_recalls.values())/len(norm_recalls):<20.4f} {sum(norm_macro_f1_score.values())/len(norm_macro_f1_score):<20.4f} {sum([len(s) for s in precision.label_sets['norm'].values()]):<20}")

if __name__ == "__main__":
    main()
    
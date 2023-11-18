from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

class GTokenizer():
    def __init__(self, plm = "EleutherAI/pythia-70m", revision="step3000"):
        self.plm = "EleutherAI/pythia-70m" #"EleutherAI/pythia-70m-deduped"
        self.bos = '<|endoftext|>'
        self.eos = '<|END|>'
        self.pad = '<|pad|>'
        self.sep ='\n\n####\n\n'

        special_tokens_dict = {'eos_token': self.eos, 'bos_token': self.bos, 'pad_token': self.pad, 'sep_token': self.sep}

        self.tokenizer = AutoTokenizer.from_pretrained(plm, revision=revision)
        self.tokenizer.padding_side = "left"
        self.tokenizer.add_special_tokens(special_tokens_dict)
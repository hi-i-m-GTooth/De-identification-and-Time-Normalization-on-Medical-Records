import os

from train import writeValidPredictions, getTokenizer
from parse_args import parse_args_infer
from transformers import AutoTokenizer, AutoModelForCausalLM

current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

def main():
    args = parse_args_infer()
    tokenizer = getTokenizer()
    model = AutoModelForCausalLM.from_pretrained(args.model_dir)
    model.resize_token_embeddings(len(tokenizer))
    model.eval()
    model.to(args.device)
    writeValidPredictions(model, tokenizer, path = os.path.join(args.output_dir, "answer.txt"), dataset = args.infer_file, batch_size=args.batch_size)

if __name__ == "__main__":
    main()
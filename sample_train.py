from tqdm import tqdm,trange
import os

from parse_args import parse_args
from gtokenizer import GTokenizer

import torch
from torch.utils.data import DataLoader
from torch.optim import AdamW

from islab.aicup import collate_batch_with_prompt_template, OpenDeidBatchSampler
from islab.aicup import aicup_predict

from datasets import load_dataset, Features, Value
from transformers import AutoConfig
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import get_linear_schedule_with_warmup

# get current file path
cur_path = os.path.abspath(__file__)
# get current file directory
cur_dir = os.path.dirname(cur_path)
os.chdir(cur_dir)

PLM = "EleutherAI/pythia-70m"
REVISION = "step3000"

def getTrainDataset():
    dataset = load_dataset("csv", data_files="./data/train.gsv", delimiter='{{}}',
                           features = Features({
                               'fid': Value('string'), 'idx': Value('int64'),
                               'content': Value('string'), 'label': Value('string')}),
                               column_names=['fid', 'idx', 'content', 'label'], keep_default_na=False)
    
    return dataset

def getTokenizer():
    return GTokenizer(plm = PLM, revision=REVISION).tokenizer

# def getDataLoader(dataset, tokenizer, batch_size=3, shuffle=False):
#     return DataLoader(dataset, batch_size=batch_size, collate_fn=lambda batch: collate_batch_with_prompt_template(batch, tokenizer))

# Bucket dataloader
def getDataLoader(dataset, tokenizer, batch_size=8, shuffle=False):
    return DataLoader(dataset, batch_sampler=OpenDeidBatchSampler(dataset, batch_size),
                    collate_fn=lambda batch: collate_batch_with_prompt_template(batch, tokenizer), pin_memory=True)

def getModel(tokenizer):
    config = AutoConfig.from_pretrained(PLM, 
                                        bos_token_id=tokenizer.bos_token_id,
                                        eos_token_id=tokenizer.eos_token_id,
                                        pad_token_id=tokenizer.pad_token_id,
                                        sep_token_id=tokenizer.sep_token_id,
                                        output_hidden_states=False)
    model = AutoModelForCausalLM.from_pretrained(PLM, revision=REVISION, config=config)
    return model

def trainModel(model, dataloader, optimizer, epoch, device):
    model.train()
    for _ in trange(epoch, desc="Epoch"):
        total_loss = 0
        # Training loop
        predictions , true_labels = [], []

        for step, (seqs, labels, masks) in enumerate(dataloader):
            seqs = seqs.to(device)
            labels = labels.to(device)
            masks = masks.to(device)
            model.zero_grad()
            outputs = model(seqs, labels=labels, attention_mask=masks)
            logits = outputs.logits
            loss = outputs.loss
            loss = loss.mean()

            total_loss += loss.item()
            loss.backward()
            optimizer.step()

        avg_train_loss = total_loss / len(dataloader)
        print("Average train loss: {}".format(avg_train_loss))

def writeValidPredictions(model, tokenizer, path = "./submissions/test_answer.txt"):
    BATCH_SIZE = 32
    valid_data = load_dataset("csv", data_files="./data/examples/opendid_valid.tsv", delimiter='\t',
                    features = Features({
                    'fid': Value('string'), 'idx': Value('int64'),
                    'content': Value('string'), 'label': Value('string')}),
                    column_names=['fid', 'idx', 'content', 'label'])
    valid_list = list(valid_data['train'])

    with open(path, 'w', encoding='utf8') as f:
        for i in tqdm(range(0, len(valid_list), BATCH_SIZE)):
            with torch.no_grad():
                seeds = valid_list[i:i+BATCH_SIZE]
                outputs = aicup_predict(model, tokenizer, input=seeds)
                for o in outputs:
                    f.write(o)
                    f.write('\n')

def Main():
    args = parse_args()
    device = torch.device(args.device if torch.cuda.is_available() else "cpu")
    sub_size = args.subdataset_size
    print(f"Device: {device}")

    dataset = getTrainDataset()
    if sub_size == -1:
        sub_size = len(dataset['train'])
    sub_datasets = torch.utils.data.random_split(dataset['train'], [sub_size, len(dataset['train']) - sub_size])
    print(f"Sample Dataset / Full Dataset: {len(sub_datasets[0])}/{len(dataset['train'])}")

    tokenizer = getTokenizer()
    dataloader = getDataLoader(sub_datasets[0], tokenizer, batch_size=args.batch_size, shuffle=False)
    model = getModel(tokenizer)
    optimizer = AdamW(model.parameters(), lr=args.lr)

    model.resize_token_embeddings(len(tokenizer))
    model.to(device)

    trainModel(model, dataloader, optimizer, args.epoch, device)
    # save model
    model.save_pretrained("./model")
    
    writeValidPredictions(model, tokenizer)

if __name__ == "__main__":
    Main()
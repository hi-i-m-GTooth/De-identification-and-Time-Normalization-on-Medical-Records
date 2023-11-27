from tqdm import tqdm,trange
import time
import os
from colorama import Fore, Back, Style

from parse_args import parse_args
from gtokenizer import GTokenizer

import torch
from torch.utils.data import DataLoader
from torch.optim import AdamW

from gaicup import collate_batch_with_prompt_template, OpenDeidBatchSampler
from gaicup import aicup_predict

from datasets import load_dataset, Features, Value
from transformers import AutoConfig
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import get_linear_schedule_with_warmup

# get current file path
cur_path = os.path.abspath(__file__)
# get current file directory
cur_dir = os.path.dirname(cur_path)
os.chdir(cur_dir)

PLM = "EleutherAI/pythia-410m"
REVISION = "step3000"
VALID_BATCH_SIZE = 32

def getTrainDataset(file_name = "train.gsv"):
    dataset = load_dataset("csv", data_files=f"./data/{file_name}", delimiter='{{}}',
                           features = Features({
                               'fid': Value('string'), 'idx': Value('int64'),
                               'content': Value('string'), 'label': Value('string')}),
                               column_names=['fid', 'idx', 'content', 'label'], keep_default_na=False)
    return dataset

def getValidDataset(file_name = "valid.gsv"):
    valid_data = load_dataset("csv", data_files=f"./data/{file_name}", delimiter='{{}}',
                    features = Features({
                    'fid': Value('string'), 'idx': Value('int64'),
                    'content': Value('string'), 'label': Value('string')}),
                    column_names=['fid', 'idx', 'content', 'label'])
    return valid_data

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

def trainModel(model, dataloader, valid_dataloader, optimizer, epoch, device, exp_name, save_epoch):
    model.to(device)
    model.train()
    start_time = time.time()
    # log time in YYYY-MM-DD HH:MM:SS
    print(f"{Fore.GREEN}Start Training, Date Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}{Style.RESET_ALL}")
    prev_time = start_time
    progress_bar = trange(epoch, desc="Epoch")

    for ep in progress_bar:
        progress_bar.set_description(f"{Fore.WHITE}{Back.LIGHTGREEN_EX}[Epoch {ep+1}/{epoch}]{Style.RESET_ALL}")
        log_str = ""
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
        log_str += f"Average train loss: {Fore.BLUE}{round(avg_train_loss, 7):<10}{Style.RESET_ALL}"

        if save_epoch and (ep+1) % save_epoch == 0:
            with torch.no_grad():
                model.eval()
                total_loss = 0
                for step, (seqs, labels, masks) in enumerate(valid_dataloader):
                    seqs = seqs.to(device)
                    labels = labels.to(device)
                    masks = masks.to(device)
                    outputs = model(seqs, labels=labels, attention_mask=masks)
                    logits = outputs.logits
                    loss = outputs.loss
                    loss = loss.mean()
                    total_loss += loss.item()
                avg_valid_loss = total_loss / len(valid_dataloader)
                log_str += f" Average valid loss: {Fore.CYAN}{round(avg_valid_loss, 7):<10}{Style.RESET_ALL}"
            
            model.save_pretrained(f"./models/{exp_name}/{exp_name}_{ep+1}")

        cur_time = time.time()
        log_str += f" Time: {Fore.YELLOW}{int((cur_time - prev_time) / 60)}m {int((cur_time - prev_time)%60)}s{Style.RESET_ALL} Date Time: {Fore.YELLOW}{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}{Style.RESET_ALL}"
        prev_time = cur_time
        print(log_str)

    cur_time = time.time()
    log_str = f"{Fore.GREEN}Finish Total time: {round((cur_time - start_time)/60, 2)}m{Style.RESET_ALL}"
    print(log_str)
    print(f"{Fore.GREEN}Finish Date Time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}{Style.RESET_ALL}")

def writeValidPredictions(model, tokenizer, path = "./submissions/test_answer.txt", dataset = None, delimiter = '\t'):
    if not dataset:
        valid_data = load_dataset("csv", data_files="./data/examples/opendid_valid.tsv", delimiter='\t',
                        features = Features({
                        'fid': Value('string'), 'idx': Value('int64'),
                        'content': Value('string'), 'label': Value('string')}),
                        column_names=['fid', 'idx', 'content', 'label'])
    else:
        valid_data = getValidDataset(dataset)
    
    valid_list = list(valid_data['train'])

    with open(path, 'w', encoding='utf8') as f:
        for i in tqdm(range(0, len(valid_list), VALID_BATCH_SIZE)):
            with torch.no_grad():
                seeds = valid_list[i:i+VALID_BATCH_SIZE]
                outputs = aicup_predict(model, tokenizer, input=seeds)
                for o in outputs:
                    f.write(o)
                    f.write('\n')

def Main():
    args = parse_args()
    device = torch.device(args.device if torch.cuda.is_available() else "cpu")
    sub_size = args.subdataset_size
    exp_name = args.exp_name
    print(f"Experiment Name: {exp_name}")
    print(f"Device: {device}")

    global PLM, REVISION
    PLM = args.model_name
    REVISION = args.revision

    dataset = getTrainDataset(args.train_file)
    valid_dataset = getValidDataset(args.valid_file)

    if sub_size == -1:
        sub_size = len(dataset['train'])
    sub_datasets = torch.utils.data.random_split(dataset['train'], [sub_size, len(dataset['train']) - sub_size])
    print(f"Sample Dataset / Full Dataset: {len(sub_datasets[0])}/{len(dataset['train'])}")

    tokenizer = getTokenizer()
    dataloader = getDataLoader(sub_datasets[0], tokenizer, batch_size=args.batch_size, shuffle=False)
    valid_dataloader = getDataLoader(valid_dataset['train'], tokenizer, batch_size=VALID_BATCH_SIZE, shuffle=False)
    
    model = getModel(tokenizer)
    optimizer = AdamW(model.parameters(), lr=args.lr)

    model.resize_token_embeddings(len(tokenizer))
    model.to(device)

    trainModel(model, dataloader, valid_dataloader, optimizer, args.epoch, device, exp_name, args.save_epoch)
    # save model
    model.save_pretrained(f"./models/{exp_name}/{exp_name}_final")
    
    os.mkdir(f"./submissions/{exp_name}")
    writeValidPredictions(model, tokenizer, path = f"./submissions/{exp_name}/answer.txt")

if __name__ == "__main__":
    Main()
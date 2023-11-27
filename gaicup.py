import torch
import random
import re

def collate_batch_with_prompt_template(batch, tokenizer, template = "<|endoftext|> __CONTENT__\n\n####\n\n__LABEL__ <|END|>", IGNORED_PAD_IDX = -100):
    """ template: __CONTENT__ and __LABEL__ will be replaced with the content and the corresponding labels."""	
    # default template: {bos} {data['content']} {sep}
	
    texts = [template.replace("__LABEL__", data['label']).replace("__CONTENT__", data['content']) for data in list(batch)]
    encoded_seq = tokenizer(texts, padding=True)
    
    indexed_tks = torch.tensor(encoded_seq['input_ids'])
    attention_mask = torch.tensor(encoded_seq['attention_mask'])
    encoded_label = torch.tensor(encoded_seq['input_ids'])
    encoded_label[encoded_label == tokenizer.pad_token_id] = IGNORED_PAD_IDX
    
    return indexed_tks, encoded_label, attention_mask
def my_input():
    input()
def aicup_predict(model, tokenizer, input, template = "<|endoftext|> __CONTENT__\n\n####\n\n"):
    seeds = [template.replace("__CONTENT__", data['content']) for data in input]
    sep = tokenizer.sep_token
    eos = tokenizer.eos_token
    pad = tokenizer.pad_token
    pad_idx = tokenizer.convert_tokens_to_ids(tokenizer.pad_token)
    """Generate text from a trained model."""
    model.eval()
    device = model.device
    texts = tokenizer(seeds, return_tensors = 'pt', padding=True).to(device)
    outputs = []
    #return
    with torch.cuda.amp.autocast():
        output_tokens = model.generate(**texts, max_new_tokens=400, pad_token_id = pad_idx,
                                        eos_token_id=tokenizer.convert_tokens_to_ids(eos))
        preds = tokenizer.batch_decode(output_tokens)
        for idx , pred in enumerate(preds):
            pred = pred[pred.index(sep)+len(sep):].replace(pad, "").replace(eos, "").strip()
            if pred == "PHI: NULL":
                continue
            phis = pred.split(r'\n')
            # print(phis); my_input()
            lidxs = {}
            for p in phis:
                tid = p.find(':')
                if tid > 0:
                    text = p[tid+1:].strip()
                    if text == '':
                        continue
                    nv = text.find('=>')
                    normalizedV = None
                    if nv > 0:
                        normalizedV = text[nv+2:]
                        text = text[:nv]
                    lidx = 0
                    if text in lidxs:
                        lidx = lidxs[text]
                    content = re.sub('\[PREFIX_START\].*\[PREFIX_END\]', '', input[idx]['content'])
                    lidx = content.find(text, lidx)
                    eidx = lidx+len(text)
                    lidxs[text] = eidx
                    sidx=int(input[idx]["idx"])
                    if normalizedV is None:
                        outputs.append(f'{input[idx]["fid"]}\t{p[:tid]}\t{lidx+sidx}\t{eidx+sidx}\t{text}')
                    else:
                        outputs.append(f'{input[idx]["fid"]}\t{p[:tid]}\t{lidx+sidx}\t{eidx+sidx}\t{text}\t{normalizedV}')
    return outputs

def gpt_batch_decode(text, model, tokenizer, max_input_tokens=1000, max_output_tokens=100):
    # Tokenize
    input_ids = tokenizer.encode(text, return_tensors="pt",
          truncation=True, max_length=max_input_tokens)

    # Generate
    device = model.device
    generated_tokens_with_prompt = model.generate(input_ids=input_ids.to(device),
        pad_token_id = tokenizer.eos_token_id, max_new_tokens=max_output_tokens)

    # Decode
    generated_text_with_prompt = tokenizer.batch_decode(generated_tokens_with_prompt, skip_special_tokens=True)

    # Strip the prompt
    generated_text_answer = generated_text_with_prompt[0][len(text):]

    return generated_text_answer
   
class OpenDeidBatchSampler():    
    def __init__(self, data, batch_size):
        self.pooled_indices = []
        self.data = data
        self.batch_size = batch_size
        self.len = len(list(data))  
    def __iter__(self):
        self.pooled_indices = []
        indices = [(index, len(data["content"])) for index, data in enumerate(self.data)]
        random.shuffle(indices)
        # create pool of indices with similar lengths 
        for i in range(0, len(indices), self.batch_size * 100):
            self.pooled_indices.extend(sorted(indices[i:i + self.batch_size * 100], key=lambda x: x[1], reverse=True))
        self.pooled_indices = [x[0] for x in self.pooled_indices]

        # yield indices for current batch
        for i in range(0, len(self.pooled_indices), self.batch_size):
            yield self.pooled_indices[i:i + self.batch_size]
    def __len__(self):
        return (self.len + self.batch_size - 1) // self.batch_size   
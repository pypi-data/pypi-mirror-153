from collections import defaultdict
import json, re, string
import urllib.request

class BPE(object):
    def __init__(self):
        vocab_location = "https://beginai-demo-datasets.s3.ca-central-1.amazonaws.com/vocab.json"
        with urllib.request.urlopen(vocab_location) as url:
            data = json.loads(url.read().decode())
        vocab_stoi = data

        self.vocab_stoi = defaultdict(lambda: vocab_stoi['[UNK]'], vocab_stoi)
        self.vocab_itos = list(data.keys())

        self.unk_token = '[UNK]'
        self.pad_token = '[PAD]'
        self.sep_token = '[SEP]'
        self.cls_token = '[CLS]'

        self.unk_id = data['[UNK]']
        self.pad_id = data['[PAD]']
        self.sep_id = data['[SEP]']
        self.cls_id = data['[CLS]']

        self.preprocess = True

        # `p` for compiling punctuations
        self.p = re.compile(f'##[{string.punctuation}]')
        
    def _preprocess(self, text) -> str:
        text = text.lower()
        text = re.sub(r"\s+", " ", text)
        return text.strip()
    
    def tokenize(self, text: str) -> list:
        tokens = []
        if self.preprocess: text = self._preprocess(text)
        sentence = text.split()
        
        for word in sentence :
            chars = list(word)
            is_bad = False
            start = 0
            sub_tokens = []

            while start < len(chars):
                end = len(chars)
                cur_substr = None
                while start < end:
                    substr = "".join(chars[start:end])
                    if start > 0:
                        substr = "##" + substr
                    if len(sub_tokens) >= 1:
                        if sub_tokens[-1] in string.punctuation:
                            substr = substr[2:]
                    if substr in self.vocab_stoi:
                        cur_substr = substr
                        break
                    end -= 1
                if cur_substr is None:
                    is_bad = True
                    break
                if self.p.search(cur_substr) is not None:
                    sub_tokens.append(cur_substr[-1])
                else:
                    sub_tokens.append(cur_substr)
                start = end

            if is_bad:
                tokens.append(self.unk_token)
            else:
                tokens.extend(sub_tokens)
        return tokens
      
    
    def encode(self, text: str, padding = False, seq_len = None) -> list:

        if len(text) == 0:
            return {
                "input_ids":[], 
                "attention_mask": [], 
                "len_":0
            }
            
        encoded = [self.vocab_stoi[s] for s in self.tokenize(text)]

        if not padding:           
            return [self.cls_id] + encoded + [self.sep_id]

        seq_len -= 2

        if len(encoded) > seq_len:

            tokens = [self.cls_id] + encoded[:seq_len] + [self.sep_id]

            len_ = len(encoded[:seq_len]) + 2

            attention_mask = [1]*len_

            return {
                "input_ids":tokens, 
                "attention_mask":attention_mask, 
                "len_":len_
            } 
        else:
            padding = [self.pad_id] * (seq_len - len(encoded))

            tokens = [self.cls_id] + encoded + [self.sep_id] + padding

            len_ = len(encoded) + 2

            attention_mask = [1]*len_ + [0]*len(padding) 

            return {
                "input_ids":tokens, 
                "attention_mask":attention_mask, 
                "len_":len_
            }  
    
    def decode(self, encodings) -> str:
        tokens = [self.vocab_itos[i] for i in encodings]
        return "".join([" " + i if "##" not in i else i.replace("#", '') for i in tokens]).strip()
import numpy as np
import torch
from transformers import AutoTokenizer
from transformers import AutoModel


class PatentModel():
    def __init__(self, pretrained_name:str="anferico/bert-for-patents", use_gpu:bool=True) -> None:
        self.device     = "cuda:0" if torch.cuda.is_available() and use_gpu else "cpu"
        self.tokenizer  = AutoTokenizer.from_pretrained(pretrained_name)
        self.model      = AutoModel.from_pretrained(pretrained_name)
        self.model      = self.model.to(self.device)

    def embedding(self, text:str):
        token = self.tokenizer(text, return_tensors='pt', max_length=512, truncation=True)
        token = {k:v.to(self.device) for k, v in token.items()}
        output = self.model(**token).last_hidden_state[:, 0, :]
        return output.cpu().detach().numpy()
    
    def embedding_by_concat(self, text:str, max_lenght:int=510):
        text_list = self.split_text_by_words(text, max_lenght)
        emb_array = None
        for i in text_list:
            emb_tmp = self.embedding(i)
            if emb_array is None:
                emb_array = emb_tmp
            else:
                emb_array = np.concatenate((emb_array, emb_tmp))
        emb_output = np.mean(emb_array, axis=0)
        return emb_output
    
    def embedding_by_overlapping(self, text:str, max_lenght:int=510, overlapping_size:int=20):
        text_list = self.split_text_by_words_overlapping(text, max_lenght, overlapping_size)
        emb_array = None
        for i in text_list:
            emb_tmp = self.embedding(i)
            if emb_array is None:
                emb_array = emb_tmp
            else:
                emb_array = np.concatenate((emb_array, emb_tmp))
        emb_output = np.mean(emb_array, axis=0)
        return emb_output

    
    @staticmethod
    def split_text_by_words(text:str, max_words:int) -> list:
        split_text = []
        words = text.split()
        
        for k in range(len(words) // max_words + 1):
            start_index = k * max_words
            start_index = start_index if start_index>0 else start_index
            end_index = min(start_index + max_words, len(words))
            split_text.append(' '.join(words[start_index:end_index]))
        
        return split_text

    @staticmethod
    def split_text_by_words_overlapping(text:str, max_words:int, overlapping_size:int) -> list:
        split_text = []
        words = text.split()
        
        k=0
        start_index=0
        while len(words) > start_index+overlapping_size+1:
            start_index = k * max_words
            start_index = start_index-overlapping_size*k if start_index>0 else start_index
            end_index = min(start_index + max_words, len(words))
            split_text.append(' '.join(words[start_index:end_index]))
            k+=1
        
        return [i for i in split_text if i!=""]
    
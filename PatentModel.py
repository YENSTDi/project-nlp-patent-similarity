from transformers import AutoTokenizer
from transformers import AutoModel

class PatentModel():
    def __init__(self, pretrained_name:str="anferico/bert-for-patents") -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(pretrained_name)
        self.model = AutoModel.from_pretrained(pretrained_name)

    def embedding(self, text:str):
        token = self.tokenizer(text, return_tensors='pt', max_length=512, truncation=True)
        output = self.model(**token).last_hidden_state[:, 0, :]
        return output.detach().numpy()
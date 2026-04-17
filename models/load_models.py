import spacy
from transformers import BertTokenizer, BertModel

def load_all():
    nlp = spacy.load("en_core_web_sm")
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertModel.from_pretrained("bert-base-uncased")

    return nlp, tokenizer, model
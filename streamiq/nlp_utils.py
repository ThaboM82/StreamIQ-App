# streamiq/nlp_utils.py
from transformers import AutoTokenizer

# Load a multilingual tokenizer (good for South African languages)
tokenizer = AutoTokenizer.from_pretrained("bert-base-multilingual-cased")

def tokenize(text: str):
    """
    Tokenize input text using HuggingFace tokenizer.
    Returns token IDs and attention mask.
    """
    return tokenizer(text, padding=True, truncation=True, return_tensors="pt")

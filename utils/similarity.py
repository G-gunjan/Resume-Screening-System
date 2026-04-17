import torch
from sklearn.metrics.pairwise import cosine_similarity

def get_embedding(text, tokenizer, model):
    tokens = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**tokens)
    return outputs.last_hidden_state[:, 0, :].numpy()


def compute_similarity(job, resume, tokenizer, model):
    job_emb = get_embedding(job, tokenizer, model)
    res_emb = get_embedding(resume, tokenizer, model)

    return cosine_similarity(job_emb, res_emb)[0][0]
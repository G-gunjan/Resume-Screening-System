def preprocess_text(text, nlp):
    doc = nlp(text)
    tokens = [
        token.lemma_.lower()
        for token in doc
        if not token.is_stop and token.is_alpha
    ]
    return " ".join(tokens)
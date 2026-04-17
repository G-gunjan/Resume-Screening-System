import pdfplumber
import docx

def extract_text(file):
    if file.type == "application/pdf":
        with pdfplumber.open(file) as pdf:
            return "".join([p.extract_text() or "" for p in pdf.pages])

    else:
        doc = docx.Document(file)
        return " ".join([p.text for p in doc.paragraphs])
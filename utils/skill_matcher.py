from spacy.matcher import PhraseMatcher
from config import SKILL_SET

def setup_matcher(nlp):
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(skill) for skill in SKILL_SET]
    matcher.add("SKILLS", patterns)
    return matcher


def extract_skills(text, nlp, matcher):
    doc = nlp(text.lower())
    matches = matcher(doc)
    return list(set([doc[start:end].text for _, start, end in matches]))


def skill_gap(job_desc, resume, nlp, matcher):
    job_skills = extract_skills(job_desc, nlp, matcher)
    resume_skills = extract_skills(resume, nlp, matcher)

    matched = list(set(job_skills) & set(resume_skills))
    missing = list(set(job_skills) - set(resume_skills))

    score = len(matched) / len(job_skills) if job_skills else 0

    return score, matched, missing
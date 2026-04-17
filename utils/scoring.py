from config import TECH_WEIGHTS, NON_TECH_WEIGHTS

def calculate_score(role, sim, skill, github=0):

    if role == "Tech":
        return (
            TECH_WEIGHTS["similarity"] * sim +
            TECH_WEIGHTS["skills"] * skill +
            TECH_WEIGHTS["github"] * github
        )
    else:
        return (
            NON_TECH_WEIGHTS["similarity"] * sim +
            NON_TECH_WEIGHTS["skills"] * skill
        )
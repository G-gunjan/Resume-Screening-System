import streamlit as st
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from models.load_models import load_all
from utils.text_extractor import extract_text
from utils.preprocessing import preprocess_text
from utils.similarity import compute_similarity
from utils.skill_matcher import setup_matcher, skill_gap

#  MATCHING YOUR FILE
from utils.github_extractor import extract_github_links, extract_usernames
from utils.github_analyzer import github_score
from utils.scoring import calculate_score

from utils.charts import (
    plot_ranking,
    plot_comparison,
    plot_distribution,
    plot_top_candidates
)


# LOAD MODELS
nlp, tokenizer, model = load_all()
matcher = setup_matcher(nlp)


st.set_page_config(page_title="AI Resume Screening", layout="wide")

st.title("🚀 AI Resume Screening System")

role = st.selectbox("Select Role Type", ["Tech", "Non-Tech"])

job_desc = st.text_area("📄 Job Description")

files = st.file_uploader(
    "📂 Upload Resumes",
    type=["pdf", "docx"],
    accept_multiple_files=True
)


if st.button("Rank Candidates"):

    if not job_desc or not files:
        st.warning("⚠️ Please provide Job Description and upload resumes")
        st.stop()

    results = []

    job_processed = preprocess_text(job_desc, nlp)

    for file in files:

        text = extract_text(file)

        if not text:
            continue

        processed = preprocess_text(text, nlp)

        # Similarity
        sim = compute_similarity(job_processed, processed, tokenizer, model)

        # Skill Matching
        skill_score, matched, missing = skill_gap(job_desc, text, nlp, matcher)

        #github auto extraction
        github_links = extract_github_links(text)
        usernames = extract_usernames(github_links)

        # Take first valid username
        username = usernames[0] if usernames else None

        gh_score = github_score(username) if (role == "Tech" and username) else 0

        # Final Score
        total = calculate_score(role, sim, skill_score, gh_score)

        results.append({
            "Candidate": file.name,
            "Score": round(total, 3),
            "Similarity": round(sim, 3),
            "Skills": round(skill_score, 3),
            "GitHub": round(gh_score, 3),
            "GitHub Link": github_links[0] if github_links else "N/A",
            "Matched Skills": ", ".join(matched),
            "Missing Skills": ", ".join(missing)
        })

    if not results:
        st.error("❌ No valid resumes processed")
        st.stop()

    df = pd.DataFrame(results).sort_values(by="Score", ascending=False)

    
    # TOP CANDIDATE
    top_candidate = df.iloc[0]
    st.success(
        f"🏆 Top Candidate: {top_candidate['Candidate']} "
        f"(Score: {top_candidate['Score']})"
    )

    # FILTER
    threshold = st.slider("Minimum Score Filter", 0.0, 1.0, 0.55)

    filtered_df = df[df["Score"] >= threshold]

    st.write(f"Showing {len(filtered_df)} candidates")

  
    # TABLE
    st.subheader("📋 Candidate Ranking")
    st.dataframe(filtered_df, use_container_width=True)

    # CHARTS
    st.subheader("📊 Visual Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(plot_ranking(filtered_df), use_container_width=True)

    with col2:
        st.plotly_chart(plot_distribution(filtered_df), use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.plotly_chart(plot_comparison(filtered_df), use_container_width=True)

    with col4:
        st.plotly_chart(plot_top_candidates(filtered_df), use_container_width=True)


    st.download_button(
        "📥 Download Results CSV",
        df.to_csv(index=False),
        file_name="candidate_ranking.csv"
    )
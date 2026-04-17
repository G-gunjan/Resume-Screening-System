import plotly.express as px
import pandas as pd


# 🏆 Final Ranking Chart
def plot_ranking(df):
    fig = px.bar(
        df,
        x="Candidate",
        y="Score",
        color="Score",
        text="Score",
        title="🏆 Candidate Ranking",
    )

    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(xaxis_tickangle=-30)

    return fig


# 📊 Comparison Chart (all metrics) ✅ FIXED
def plot_comparison(df):
    df_melted = df.melt(
        id_vars="Candidate",
        value_vars=["Similarity", "Skills", "GitHub"],
        var_name="Metric",
        value_name="Metric Score"   # ✅ FIXED (no conflict with "Score")
    )

    fig = px.bar(
        df_melted,
        x="Candidate",
        y="Metric Score",   # ✅ UPDATED
        color="Metric",
        barmode="group",
        title="📊 Candidate Comparison"
    )

    fig.update_layout(xaxis_tickangle=-30)

    return fig


# 📈 Score Distribution
def plot_distribution(df):
    fig = px.histogram(
        df,
        x="Score",
        nbins=10,
        title="📈 Score Distribution"
    )

    return fig


# 🥇 Top Candidates Pie
def plot_top_candidates(df, top_n=5):

    if df.empty:
        return px.pie(title="No data available")

    top_df = df.head(top_n)

    fig = px.pie(
        top_df,
        names="Candidate",
        values="Score",
        title=f"🥇 Top {top_n} Candidates Share"
    )

    return fig
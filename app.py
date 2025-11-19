import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Main panel configuration
st.set_page_config(page_title="University Dashboard", layout="wide")
st.title("University Data Dashboard")

# Load CSV file
df = pd.read_csv("university_student_data (2).csv")

# Sidebar filters
st.sidebar.header("Filters")
year = st.sidebar.selectbox("Year", sorted(df["Year"].unique()))
terms = st.sidebar.multiselect("Term(s)", df["Term"].unique(), default=df["Term"].unique())

# Filtered dataframe
df_f = df[(df["Year"] == year) & (df["Term"].isin(terms))]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Applications", int(df_f["Applications"].sum()))
col2.metric("Retention Avg (%)", f"{df_f['Retention Rate (%)'].mean():.1f}%")
col3.metric("Satisfaction Avg (%)", f"{df_f['Student Satisfaction (%)'].mean():.1f}%")

# ===========
# GRAPH 1 — Retention Trend (ALL YEARS, FILTER BY TERM)
# ===========
st.subheader("Retention Rate Trend (%) (2015–2020)")

df_ret_year = df[df["Term"].isin(terms)]   # <-- se filtran TERM como en tu imagen original
df_ret_year = df_ret_year.groupby("Year")["Retention Rate (%)"].mean().reset_index()

fig1, ax1 = plt.subplots()
sns.lineplot(
    data=df_ret_year,
    x="Year",
    y="Retention Rate (%)",
    marker="o",
    color="royalblue",
    ax=ax1
)

ax1.grid(True, linestyle="--", alpha=0.6)
st.pyplot(fig1)

# ===========
# GRAPH 2 — Satisfaction (ALL YEARS, FILTER BY TERM)
# ===========
st.subheader("Student Satisfaction (%) (2015–2020)")

df_sat_year = df[df["Term"].isin(terms)]
df_sat_year = df_sat_year.groupby("Year")["Student Satisfaction (%)"].mean().reset_index()

fig2, ax2 = plt.subplots()
sns.barplot(
    data=df_sat_year,
    x="Year",
    y="Student Satisfaction (%)",
    hue="Year",
    palette="Blues_d",
    dodge=False,
    legend=False,
    ax=ax2
)

ax2.set_ylim(0, 100)
ax2.grid(axis="y", linestyle="--", alpha=0.6)
st.pyplot(fig2)

# ===========
# GRAPH 3 — Spring vs Fall Enrollment
# ===========
st.subheader("Enrollment distribution between Spring and Fall")

faculties = [c for c in df_f.columns if "Enrolled" in c and "Total" not in c]
if faculties:
    df_f["Tot]()_


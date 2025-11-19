import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Maain panel configuartion
st.set_page_config(page_title="University Dashboard", layout="wide")
st.title("University Data Dashboard")

# the CSV file is loaded
df = pd.read_csv("university_student_data (2).csv")
df["Year"] = df["Year"].astype(int)

# we create a interactive filters are created
st.sidebar.header("Filters")
years = st.sidebar.multiselect("Year(s)", sorted(df["Year"].unique()), default=sorted(df["Year"].unique()))
terms = st.sidebar.multiselect("Term(s)", df["Term"].unique(), default=df["Term"].unique())

df_f = df[(df["Year"].isin(years)) & (df["Term"].isin(terms))]
df_f["Year"] = df_f["Year"].astype(int)

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Applications", int(df_f["Applications"].sum()))
col2.metric("Retention Avg (%)", f"{df_f['Retention Rate (%)'].mean():.1f}%")
col3.metric("Satisfaction Avg (%)", f"{df_f['Student Satisfaction (%)'].mean():.1f}%")


#  Graph  1: Retention trend
st.subheader("Retention Rate Trend (%)")
ret_year = df_f.groupby("Year")["Retention Rate (%)"].mean().reset_index()
ret_year["Year"] = ret_year["Year"].astype(int)

fig1, ax1 = plt.subplots(figsize=(6, 3))
sns.lineplot(data=ret_year, x="Year", y="Retention Rate (%)", marker="o", ax=ax1)
ax1.set_xticks(ret_year["Year"])
ax1.set_xticklabels(ret_year["Year"])
ax1.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
st.pyplot(fig1)


st.subheader("Average Student Satisfaction (%)")
sat_year = df_f.groupby("Year")["Student Satisfaction (%)"].mean().reset_index()
sat_year["Year"] = sat_year["Year"].astype(int)

# Graph 2: Student Satisfaction by Year
fig2, ax2 = plt.subplots(figsize=(6, 3))
sns.barplot(data=sat_year, x=sat_year["Year"].astype(str), y="Student Satisfaction (%)", ax=ax2)
ax2.set_xticks(range(len(sat_year)))
ax2.set_xticklabels(sat_year["Year"])
ax2.set_ylim(0, 100)
ax2.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()
st.pyplot(fig2)

# Graph 3: Enrollment distribution between Spring and Fall
st.subheader("Enrollment distribution between Spring and Fall")
fac_cols = [c for c in df.columns if "Enrolled" in c and "Total" not in c]
df_f["Total Enrolled"] = df_f[fac_cols].sum(axis=1)

term_group = df_f.groupby("Term", as_index=False)["Total Enrolled"].sum()

if not term_group.empty:
    fig3, ax3 = plt.subplots(figsize=(4, 4))
    ax3.pie(term_group["Total Enrolled"], labels=term_group["Term"], autopct="%1.1f%%", startangle=90)
    st.pyplot(fig3)
else:
    st.warning("No data available for the selected filters.")

# Table 4: Filtereed data according to the selected criteria
# We include this small table as part of the dashboard to display the filtered data in detail
st.subheader("Filtered Data")
st.dataframe(df_f, use_container_width=True)






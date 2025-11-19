import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="University Dashboard", layout="wide")
st.title(" University Data Dashboard")

df = pd.read_csv("university_student_data (2).csv")

st.sidebar.header("Filters")
year = st.sidebar.selectbox("Year", sorted(df["Year"].unique()))
terms = st.sidebar.multiselect("Term(s)", df["Term"].unique(), default=df["Term"].unique())

df_f = df[(df["Year"] == year) & (df["Term"].isin(terms))]

col1, col2, col3 = st.columns(3)
col1.metric("Applications", int(df_f["Applications"].sum()))
col2.metric("Retention Avg (%)", f"{df_f['Retention Rate (%)'].mean():.1f}%")
col3.metric("Satisfaction Avg (%)", f"{df_f['Student Satisfaction (%)'].mean():.1f}%")

# 1) Retention trend (DYNAMIC)
grp_year = (df_sub.groupby('Year')
            .apply(lambda g: wavg(g['Retention Rate (%)'], g['Enrolled']))
            .rename("Retention_w")
            .sort_index())

fig1, ax1 = plt.subplots(figsize=(10, 5))
x_idx = np.arange(len(grp_year.index))
ax1.plot(x_idx, grp_year.values, marker="o", linestyle="-", color=color, linewidth=2)

ax1.set_xticks(x_idx)
ax1.set_xticklabels([str(int(y)) for y in grp_year.index])
ax1.set_xlabel("Year")
ax1.set_ylabel("Retention Rate (%)")
title1 = "Weighted retention by year"
title1 += f" · up to {year_sel}" if mode == "Cumulative up to year" else f" · year {year_sel}"
ax1.set_title(title1)
ax1.grid(show_grid)
fig1.tight_layout()
st.pyplot(fig1)

# 2) Student Satisfaction (DYNAMIC)
st.subheader("Student Satisfaction (%) for Year")
sat = df[df["Term"].isin(terms)].groupby("Year")["Student Satisfaction (%)"].mean().reset_index()

fig2, ax2 = plt.subplots()
sns.barplot(
    data=sat,
    x="Year",
    y="Student Satisfaction (%)",
    palette="Blues_d",
    ax=ax2
)
ax2.set_ylim(0, 100)
ax2.grid(axis="y", linestyle="--", alpha=0.6)
st.pyplot(fig2)

# 3) Spring vs Fall (DYNAMIC)
st.subheader("Enrollment distribution between Spring and Fall")

faculties = [c for c in df_f.columns if "Enrolled" in c and "Total" not in c]
df_f["Total Enrolled"] = df_f[faculties].sum(axis=1)

comp_term = df_f.groupby("Term", as_index=False)["Total Enrolled"].sum()

if not comp_term.empty and comp_term["Total Enrolled"].sum() > 0:
    fig3, ax3 = plt.subplots()
    ax3.pie(
        comp_term["Total Enrolled"],
        labels=comp_term["Term"],
        autopct="%1.1f%%",
        startangle=90,
        colors=sns.color_palette("pastel")
    )
    st.pyplot(fig3)
else:
    st.warning("No data available for the selected filters")

st.subheader("Filtered data according to the selected criteria")
st.dataframe(df_f, use_container_width=True)


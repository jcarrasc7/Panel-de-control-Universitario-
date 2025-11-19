import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Maain panel configuartion
st.set_page_config(page_title="University Dashboard", layout="wide")
st.title(" University Data Dashboard")

# the CSV file is loaded
df = pd.read_csv("university_student_data (2).csv")

# we create a interactive filters are created
st.sidebar.header("Filters")
year = st.sidebar.selectbox("Year", sorted(df["Year"].unique()))
terms = st.sidebar.multiselect("Term(s)", df["Term"].unique(), default=df["Term"].unique())
df_f = df[(df["Year"] == year) & (df["Term"].isin(terms))]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Applications", int(df_f["Applications"].sum()))
col2.metric("Retention Avg (%)", f"{df_f['Retention Rate (%)'].mean():.1f}%")
col3.metric("Satisfaction Avg (%)", f"{df_f['Student Satisfaction (%)'].mean():.1f}%")

#  Graph  1: Retention trend
st.subheader("Retention Rate Trend (%) for Year")
fig1, ax1 = plt.subplots()
sns.lineplot(data=df.groupby("Year")["Retention Rate (%)"].mean().reset_index(),
             x="Year", y="Retention Rate (%)", marker="o", color="royalblue", ax=ax1)
ax1.grid(True, linestyle="--", alpha=0.6)
st.pyplot(fig1)

# Graph 2: Student Satisfaction by Year
st.subheader("Student Satisfaction (%) for Year")
fig2, ax2 = plt.subplots()
sns.barplot(data=df.groupby("Year")["Student Satisfaction (%)"].mean().reset_index(),
            x="Year", y="Student Satisfaction (%)", hue="Year",
            palette="Blues_d", dodge=False, legend=False, ax=ax2)
ax2.set_ylim(0,100); ax2.grid(axis="y", linestyle="--", alpha=0.6)
st.pyplot(fig2)

# Graph 3: Enrollment distribution between Spring and Fall
st.subheader("Enrollment distribution between Spring and Fall")


# the Total Enrolled column is calculated based on the data
faculties = [c for c in df_f.columns if "Enrolled" in c and "Total" not in c]
if faculties:
    df_f["Total Enrolled"] = df_f[faculties].sum(axis=1)
else:
    st.error("No columns found with 'Enrolled'")

# Group by term (Spring/Fall)
comp_term = df_f.groupby("Term", as_index=False)["Total Enrolled"].sum()

# Validate that data exists
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

# Table 4: Filtereed data according to the selected criteria
# We include this small table as part of the dashboard to display the filtered data in detail
st.subheader("Filtered data according to the selected criteria")
st.dataframe(df_f, use_container_width=True)

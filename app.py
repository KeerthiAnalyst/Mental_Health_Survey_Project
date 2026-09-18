import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Mental Health in Tech Survey",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# CUSTOM PURPLE THEME
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #F3EFF8;
}

[data-testid="stSidebar"] {
    background-color: #E4DDF0;
}

h1, h2, h3 {
    color: #4B3869;
}

[data-testid="stMetric"] {
    background-color: white;
    border-radius: 12px;
    padding: 15px;
    border: 1px solid #D6CBE5;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv("survey.csv")


# ============================================================
# DATA CLEANING
# ============================================================

# Keep realistic working-age respondents
df = df[
    (df["Age"] >= 18) &
    (df["Age"] <= 65)
].copy()


# Gender cleaning
df["Gender_clean"] = (
    df["Gender"]
    .astype(str)
    .str.strip()
    .str.lower()
)

df["Gender_clean"] = df["Gender_clean"].replace({
    "male": "Male",
    "m": "Male",
    "man": "Male",

    "female": "Female",
    "f": "Female",
    "woman": "Female"
})

df.loc[
    ~df["Gender_clean"].isin(["Male", "Female"]),
    "Gender_clean"
] = "Other"


# Fill missing values
if "self_employed" in df.columns:
    df["self_employed"] = df["self_employed"].fillna("Unknown")

if "work_interfere" in df.columns:
    df["work_interfere"] = df["work_interfere"].fillna(
        "Not applicable"
    )


# ============================================================
# PAGE TITLE
# ============================================================

st.title("Mental Health in Tech Survey")

st.write(
    "Exploratory analysis of mental health and workplace factors "
    "in the tech industry."
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("Dashboard Filters")


# Treatment filter
treatment_filter = st.sidebar.selectbox(
    "Received Mental Health Treatment?",
    ["All"] + sorted(
        df["treatment"]
        .dropna()
        .unique()
        .tolist()
    )
)


# Gender filter
gender_filter = st.sidebar.selectbox(
    "Gender",
    ["All"] + sorted(
        df["Gender_clean"]
        .dropna()
        .unique()
        .tolist()
    )
)


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()


if treatment_filter != "All":

    filtered_df = filtered_df[
        filtered_df["treatment"] == treatment_filter
    ]


if gender_filter != "All":

    filtered_df = filtered_df[
        filtered_df["Gender_clean"] == gender_filter
    ]


# ============================================================
# KEY METRICS
# ============================================================

col1, col2, col3 = st.columns(3)


# Total responses
col1.metric(
    "Total Responses",
    len(filtered_df)
)


# Treatment count
treatment_count = (
    filtered_df["treatment"] == "Yes"
).sum()


col2.metric(
    "Mental Health Treatment",
    treatment_count
)


# Treatment rate
if len(filtered_df) > 0:

    treatment_rate = (
        treatment_count /
        len(filtered_df)
    ) * 100

else:

    treatment_rate = 0


col3.metric(
    "Treatment Rate",
    f"{treatment_rate:.1f}%"
)


# ============================================================
# 1. TREATMENT RATE BY COUNTRY
# ============================================================

st.subheader(
    "Treatment Rate by Country (20+ Respondents)"
)


country_summary = (
    filtered_df
    .groupby("Country")
    .agg(
        Respondents=("treatment", "count"),
        Treatment_Rate=(
            "treatment",
            lambda x: (x == "Yes").mean() * 100
        )
    )
)


country_summary = country_summary[
    country_summary["Respondents"] >= 20
]


plot_data = country_summary.sort_values(
    "Treatment_Rate",
    ascending=True
)


fig = px.bar(
    plot_data,
    x="Treatment_Rate",
    y=plot_data.index,
    orientation="h",
    text="Treatment_Rate",
    hover_data={
        "Treatment_Rate": ":.1f",
        "Respondents": True
    }
)


fig.update_traces(
    marker_color="#7B68A8",
    texttemplate="%{text:.0f}%",
    textposition="outside"
)


fig.update_layout(
    xaxis_title="Treatment Rate (%)",
    yaxis_title="Country",
    xaxis_range=[0, 80],
    height=500,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=20, r=40, t=30, b=20)
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# 2. AGE DISTRIBUTION
# ============================================================

st.subheader(
    "Age Distribution of Respondents"
)


fig, ax = plt.subplots(
    figsize=(9, 5)
)


sns.histplot(
    filtered_df["Age"].dropna(),
    bins=30,
    color="#7B68A8",
    kde=True,
    ax=ax
)


ax.set_title(
    "Age Distribution of Respondents"
)

ax.set_xlabel(
    "Age"
)

ax.set_ylabel(
    "Number of Respondents"
)


plt.tight_layout()

st.pyplot(
    fig,
    use_container_width=True
)

plt.close(fig)


# ============================================================
# 3. RESPONDENTS BY GENDER
# ============================================================

st.subheader(
    "Respondents by Gender"
)


gender_counts = (
    filtered_df["Gender_clean"]
    .value_counts()
)


fig, ax = plt.subplots(
    figsize=(8, 5)
)


sns.barplot(
    x=gender_counts.index,
    y=gender_counts.values,
    color="#8E7DBE",
    ax=ax
)


for i, v in enumerate(
    gender_counts.values
):

    ax.text(
        i,
        v + 10,
        str(v),
        ha="center",
        fontweight="bold"
    )


ax.set_title(
    "Respondents by Gender"
)

ax.set_xlabel(
    "Gender"
)

ax.set_ylabel(
    "Number of Respondents"
)


plt.tight_layout()

st.pyplot(
    fig,
    use_container_width=True
)

plt.close(fig)


# ============================================================
# 4. MENTAL HEALTH TREATMENT DISTRIBUTION
# ============================================================

st.subheader(
    "Have You Sought Treatment for a Mental Health Condition?"
)


counts = (
    filtered_df["treatment"]
    .value_counts()
)


fig, ax = plt.subplots(
    figsize=(6, 5)
)


ax.pie(
    counts,
    labels=counts.index,
    autopct="%1.1f%%",
    colors=[
        "#7B68A8",
        "#B8B0C8"
    ],
    startangle=90,
        radius=0.75
)


plt.tight_layout()

st.pyplot(
    fig,
    use_container_width=True
)

plt.close(fig)


# ============================================================
# 5. TOP 10 COUNTRIES BY RESPONDENTS
# ============================================================

st.subheader(
    "Top 10 Countries by Number of Respondents"
)


country_counts = (
    filtered_df["Country"]
    .value_counts()
    .head(10)
)


fig, ax = plt.subplots(
    figsize=(9, 5.5)
)


sns.barplot(
    x=country_counts.values,
    y=country_counts.index,
    color="#8E7DBE",
    ax=ax
)


for i, v in enumerate(
    country_counts.values
):

    ax.text(
        v + 10,
        i,
        str(v),
        va="center",
        fontweight="bold"
    )


ax.set_title(
    "Top 10 Countries by Number of Respondents"
)

ax.set_xlabel(
    "Number of Respondents"
)

ax.set_ylabel(
    "Country"
)


plt.tight_layout()

st.pyplot(
    fig,
    use_container_width=True
)

plt.close(fig)


# ============================================================
# 6. TREATMENT RATE BY US STATE
# ============================================================

st.subheader(
    "Treatment Rate by US State (20+ Respondents)"
)


if "state" in filtered_df.columns:

    state_summary = (
        filtered_df[
            filtered_df["Country"] == "United States"
        ]
        .groupby("state")
        .agg(
            Respondents=("treatment", "count"),
            Treatment_Rate=(
                "treatment",
                lambda x: (x == "Yes").mean() * 100
            )
        )
    )


    state_summary = state_summary[
        state_summary["Respondents"] >= 20
    ]


    plot_data = state_summary.sort_values(
        "Treatment_Rate",
        ascending=True
    )


    fig, ax = plt.subplots(
        figsize=(9, 6)
    )


    sns.barplot(
        x=plot_data["Treatment_Rate"],
        y=plot_data.index,
        color="#7B68A8",
        ax=ax
    )


    for i, (rate, n) in enumerate(
        zip(
            plot_data["Treatment_Rate"],
            plot_data["Respondents"]
        )
    ):

        ax.text(
            rate + 1,
            i,
            f"{rate:.0f}% (n={n})",
            va="center",
            fontsize=9
        )


    ax.set_title(
        "Treatment Rate by US State (20+ Respondents)"
    )

    ax.set_xlabel(
        "Treatment Rate (%)"
    )

    ax.set_ylabel(
        "State"
    )

    ax.set_xlim(
        0,
        80
    )


    plt.tight_layout()

    st.pyplot(
        fig,
        use_container_width=True
    )

    plt.close(fig)

else:

    st.info(
        "State information is not available in the dataset."
    )


# ============================================================
# 7. TREATMENT RATE BY KEY FACTORS
# ============================================================

st.subheader(
    "Treatment Rate by Key Factors"
)


factors = [
    "family_history",
    "Gender_clean",
    "benefits",
    "care_options",
    "anonymity",
    "work_interfere"
]


titles = [
    "Family History of Mental Illness",
    "Gender",
    "Employer Provides Benefits",
    "Aware of Care Options",
    "Anonymity Protected",
    "Work Interference"
]


fig, axes = plt.subplots(
    3,
    2,
    figsize=(13, 14)
)


axes = axes.flatten()


for ax, factor, title in zip(
    axes,
    factors,
    titles
):

    rates = (
        filtered_df
        .groupby(factor)["treatment"]
        .apply(
            lambda x:
            (x == "Yes").mean() * 100
        )
    )


    # Logical order for work interference
    if factor == "work_interfere":

        cat_order = [
            "Never",
            "Rarely",
            "Sometimes",
            "Often",
            "Not applicable"
        ]

        rates = rates.reindex(
            [
                c
                for c in cat_order
                if c in rates.index
            ]
        )


    sns.barplot(
        x=rates.index,
        y=rates.values,
        color="#7B68A8",
        ax=ax
    )


    for i, v in enumerate(
        rates.values
    ):

        ax.text(
            i,
            v + 1.5,
            f"{v:.0f}%",
            ha="center",
            fontsize=9,
            fontweight="bold"
        )


    ax.set_title(
        f"Treatment Rate by {title}"
    )

    ax.set_ylabel(
        "Treatment Rate (%)"
    )

    ax.set_xlabel(
        ""
    )

    ax.set_ylim(
        0,
        100
    )

    ax.tick_params(
        axis="x",
        rotation=20
    )


plt.tight_layout()

st.pyplot(
    fig,
    use_container_width=True
)

plt.close(fig)


# ============================================================
# 8. TREATMENT RATE BY COMPANY SIZE
# ============================================================

st.subheader(
    "Treatment Rate by Company Size"
)


size_rates = (
    filtered_df
    .groupby("no_employees")["treatment"]
    .apply(
        lambda x:
        (x == "Yes").mean() * 100
    )
)


fig, ax = plt.subplots(
    figsize=(9, 5)
)


sns.barplot(
    x=size_rates.index,
    y=size_rates.values,
    color="#7B68A8",
    ax=ax
)


for i, v in enumerate(
    size_rates.values
):

    ax.text(
        i,
        v + 1,
        f"{v:.1f}%",
        ha="center",
        fontweight="bold"
    )


ax.set_title(
    "Treatment Rate by Company Size"
)

ax.set_xlabel(
    "Number of Employees"
)

ax.set_ylabel(
    "Treatment Rate (%)"
)

ax.set_ylim(
    0,
    70
)


plt.tight_layout()

st.pyplot(
    fig,
    use_container_width=True
)

plt.close(fig)


# ============================================================
# 9. TREATMENT RATE BY WORKPLACE WELLNESS PROGRAM
# ============================================================

st.subheader(
    "Treatment Rate by Workplace Wellness Program"
)


wellness_rates = (
    filtered_df
    .groupby("wellness_program")["treatment"]
    .apply(
        lambda x:
        (x == "Yes").mean() * 100
    )
)


fig, ax = plt.subplots(
    figsize=(8, 5)
)


sns.barplot(
    x=wellness_rates.index,
    y=wellness_rates.values,
    color="#7B68A8",
    ax=ax
)


for i, v in enumerate(
    wellness_rates.values
):

    ax.text(
        i,
        v + 1,
        f"{v:.1f}%",
        ha="center",
        fontweight="bold"
    )


ax.set_title(
    "Treatment Rate by Workplace Wellness Program"
)

ax.set_xlabel(
    "Employer Provides Wellness Program"
)

ax.set_ylabel(
    "Treatment Rate (%)"
)

ax.set_ylim(
    0,
    70
)


plt.tight_layout()

st.pyplot(
    fig,
    use_container_width=True
)

plt.close(fig)

# ============================================================
# KEY INSIGHTS
# ============================================================

st.subheader("Key Insights")

st.markdown("""
- **Treatment:** Around half of the respondents reported seeking
  treatment for a mental health condition.

- **Family history:** Respondents with a family history of mental
  illness show a different treatment pattern compared with those
  without a family history.

- **Work interference:** Treatment rates vary across levels of
  work interference, indicating a relationship between workplace
  impact and treatment-seeking behaviour.

- **Workplace support:** Access to benefits, care options and
  anonymity shows differences in treatment rates.

- **Company size:** Treatment rates vary across different company
  sizes, suggesting that workplace environment and available
  support may differ by organization size.
""")


# ============================================================
# BUSINESS SUMMARY
# ============================================================

st.subheader("Summary")

st.write("""
The analysis examines mental health treatment-seeking behaviour
among technology-sector respondents and explores how it varies
across demographic and workplace factors.

The findings highlight the importance of workplace awareness,
access to mental health resources, supportive policies and
confidentiality. The analysis is based on survey responses and
shows associations between variables rather than proving
cause-and-effect relationships.
""")


# ============================================================
# RECOMMENDATIONS
# ============================================================

st.subheader("Recommendations")

st.markdown("""
### 1. Improve Awareness
Organizations can make employees more aware of available
mental health resources, benefits and support programs.

### 2. Strengthen Confidentiality
Clear communication about privacy and anonymity may help employees
feel more comfortable seeking support.

### 3. Provide Accessible Support
Companies can provide easily accessible information about
counselling and employee assistance resources.

### 4. Reduce Workplace Barriers
Organizations can review workload, work environment and policies
when employees report that mental health affects their work.

### 5. Monitor Workplace Support
HR and leadership teams can periodically evaluate whether
employees know about and can access available mental health
resources.
""")


# ============================================================
# CONCLUSION
# ============================================================

st.subheader("Conclusion")

st.write("""
Mental health treatment-seeking behaviour varies across several
personal and workplace factors in the survey. The analysis
suggests that awareness, accessibility, confidentiality and
workplace support are important areas for organizations to
consider.

These findings can help technology organizations identify areas
where workplace mental health support and communication may be
strengthened.
""")
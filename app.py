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

[data-testid="stMetricValue"] {
    color: #4B3869;
}

.insight-box {
    background-color: white;
    padding: 18px;
    border-radius: 12px;
    border-left: 5px solid #7B68A8;
    margin-bottom: 12px;
}

.info-box {
    background-color: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #D6CBE5;
}

.footer {
    text-align: center;
    color: #6B6178;
    padding: 25px 0 10px 0;
    font-size: 14px;
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

st.title("🧠 Mental Health in Tech Survey")

st.write(
    "Exploratory analysis of mental health and workplace factors "
    "in the technology industry."
)


# ============================================================
# ABOUT THE DATA
# ============================================================

with st.expander("ℹ️ About the Dataset", expanded=True):

    st.markdown("""
    **Project Objective**

    This dashboard explores mental health treatment-seeking behaviour
    among respondents working in the technology sector and examines
    how it varies across demographic and workplace factors.

    **Key areas analyzed**

    - Mental health treatment
    - Family history of mental illness
    - Work interference
    - Workplace mental health benefits
    - Care options and anonymity
    - Company size
    - Wellness programs
    - Geographic patterns

    **Important note:** This is survey-based observational data.
    The relationships shown in this dashboard represent associations
    and should not be interpreted as proof of cause and effect.
    """)


# ============================================================
# HOW TO USE DASHBOARD
# ============================================================

with st.expander("📊 How to Use This Dashboard"):

    st.markdown("""
    Use the filters in the left sidebar to explore the data by:

    - **Mental Health Treatment**
    - **Gender**

    The charts and KPI cards update based on the selected filters.

    Hover over charts where applicable to view additional details.
    """)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("Dashboard Filters")

st.sidebar.caption(
    "Use these filters to explore the survey responses."
)


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
# FILTER STATUS
# ============================================================

active_filters = []

if treatment_filter != "All":
    active_filters.append(
        f"Treatment: {treatment_filter}"
    )

if gender_filter != "All":
    active_filters.append(
        f"Gender: {gender_filter}"
    )

if active_filters:

    st.info(
        "Active filters: " +
        " | ".join(active_filters)
    )


# ============================================================
# KEY METRICS
# ============================================================

st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)


# Total responses
col1.metric(
    "Total Responses",
    f"{len(filtered_df):,}"
)


# Treatment count
treatment_count = (
    filtered_df["treatment"] == "Yes"
).sum()


col2.metric(
    "Mental Health Treatment",
    f"{treatment_count:,}"
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
# RESPONDENT PROFILE
# ============================================================

st.header("👥 Respondent Profile")


# ============================================================
# AGE DISTRIBUTION
# ============================================================

st.subheader("Age Distribution of Respondents")


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


ax.set_xlabel("Age")
ax.set_ylabel("Number of Respondents")

ax.grid(
    axis="y",
    alpha=0.2
)

plt.tight_layout()

st.pyplot(
    fig,
    use_container_width=True
)

plt.close(fig)


# ============================================================
# RESPONDENTS BY GENDER
# ============================================================

st.subheader("Respondents by Gender")


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
        v + max(gender_counts.values) * 0.02,
        str(v),
        ha="center",
        fontweight="bold"
    )


ax.set_xlabel("Gender")
ax.set_ylabel("Number of Respondents")

ax.grid(
    axis="y",
    alpha=0.2
)

plt.tight_layout()

st.pyplot(
    fig,
    use_container_width=True
)

plt.close(fig)


# ============================================================
# TOP 10 COUNTRIES
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
        v + max(country_counts.values) * 0.01,
        i,
        str(v),
        va="center",
        fontweight="bold"
    )


ax.set_xlabel("Number of Respondents")
ax.set_ylabel("Country")

ax.grid(
    axis="x",
    alpha=0.2
)

plt.tight_layout()

st.pyplot(
    fig,
    use_container_width=True
)

plt.close(fig)


# ============================================================
# MENTAL HEALTH TREATMENT
# ============================================================

st.header("🧠 Mental Health Treatment")


# ============================================================
# TREATMENT DISTRIBUTION
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
# TREATMENT RATE BY COUNTRY
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


if not plot_data.empty:

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
        margin=dict(
            l=20,
            r=40,
            t=30,
            b=20
        )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info(
        "No countries meet the minimum 20 respondent threshold "
        "for the current filters."
    )


# ============================================================
# TREATMENT RATE BY US STATE
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


    if not plot_data.empty:

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

        ax.grid(
            axis="x",
            alpha=0.2
        )


        plt.tight_layout()

        st.pyplot(
            fig,
            use_container_width=True
        )

        plt.close(fig)

    else:

        st.info(
            "No US states meet the minimum 20 respondent "
            "threshold for the current filters."
        )

else:

    st.info(
        "State information is not available in the dataset."
    )


# ============================================================
# WORKPLACE FACTORS
# ============================================================

st.header("💼 Workplace Factors")


# ============================================================
# TREATMENT RATE BY KEY FACTORS
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

    if factor not in filtered_df.columns:
        ax.set_visible(False)
        continue


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

    ax.set_xlabel("")

    ax.set_ylim(
        0,
        100
    )

    ax.tick_params(
        axis="x",
        rotation=20
    )

    ax.grid(
        axis="y",
        alpha=0.2
    )


plt.tight_layout()

st.pyplot(
    fig,
    use_container_width=True
)

plt.close(fig)


# ============================================================
# COMPANY SIZE
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

ax.grid(
    axis="y",
    alpha=0.2
)


plt.tight_layout()

st.pyplot(
    fig,
    use_container_width=True
)

plt.close(fig)


# ============================================================
# WELLNESS PROGRAM
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

ax.grid(
    axis="y",
    alpha=0.2
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

st.header("💡 Key Insights")


# ------------------------------------------------------------
# Insight 1 - Overall Treatment
# ------------------------------------------------------------

st.markdown(
    f"""
    <div class="insight-box">
    <b>1. Mental Health Treatment</b><br>
    {treatment_count:,} out of {len(filtered_df):,} respondents
    reported seeking treatment for a mental health condition,
    representing a treatment rate of <b>{treatment_rate:.1f}%</b>.
    </div>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------------
# Insight 2 - Family History
# ------------------------------------------------------------

if "family_history" in filtered_df.columns:

    family_rates = (
        filtered_df
        .groupby("family_history")["treatment"]
        .apply(
            lambda x:
            (x == "Yes").mean() * 100
        )
    )

    if len(family_rates) >= 2:

        family_text = "<br>".join(
            [
                f"<b>{group}:</b> {rate:.1f}% treatment rate"
                for group, rate
                in family_rates.items()
            ]
        )

        st.markdown(
            f"""
            <div class="insight-box">
            <b>2. Family History</b><br>
            Treatment rates differed across family-history groups:<br>
            {family_text}
            </div>
            """,
            unsafe_allow_html=True
        )


# ------------------------------------------------------------
# Insight 3 - Work Interference
# ------------------------------------------------------------

if "work_interfere" in filtered_df.columns:

    work_rates = (
        filtered_df
        .groupby("work_interfere")["treatment"]
        .apply(
            lambda x:
            (x == "Yes").mean() * 100
        )
    )

    work_rates = work_rates.dropna()

    if not work_rates.empty:

        highest_work_group = work_rates.idxmax()
        highest_work_rate = work_rates.max()

        st.markdown(
            f"""
            <div class="insight-box">
            <b>3. Work Interference</b><br>
            The highest observed treatment rate was
            <b>{highest_work_rate:.1f}%</b> among respondents in the
            <b>{highest_work_group}</b> work-interference group.
            </div>
            """,
            unsafe_allow_html=True
        )


# ------------------------------------------------------------
# Insight 4 - Benefits
# ------------------------------------------------------------

if "benefits" in filtered_df.columns:

    benefit_rates = (
        filtered_df
        .groupby("benefits")["treatment"]
        .apply(
            lambda x:
            (x == "Yes").mean() * 100
        )
    )

    if not benefit_rates.empty:

        benefit_text = "<br>".join(
            [
                f"<b>{group}:</b> {rate:.1f}%"
                for group, rate
                in benefit_rates.items()
            ]
        )

        st.markdown(
            f"""
            <div class="insight-box">
            <b>4. Workplace Benefits</b><br>
            Treatment rates differed across employer mental-health
            benefit groups:<br>
            {benefit_text}
            </div>
            """,
            unsafe_allow_html=True
        )


# ------------------------------------------------------------
# Insight 5 - Company Size
# ------------------------------------------------------------

if "no_employees" in filtered_df.columns:

    company_rates = (
        filtered_df
        .groupby("no_employees")["treatment"]
        .apply(
            lambda x:
            (x == "Yes").mean() * 100
        )
    )

    if not company_rates.empty:

        company_text = "<br>".join(
            [
                f"<b>{group}:</b> {rate:.1f}%"
                for group, rate
                in company_rates.items()
            ]
        )

        st.markdown(
            f"""
            <div class="insight-box">
            <b>5. Company Size</b><br>
            Treatment rates varied across company-size groups:<br>
            {company_text}
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# BUSINESS IMPLICATIONS
# ============================================================

# ============================================================
# BUSINESS IMPLICATIONS
# ============================================================

st.header("📌 Business Implications")

st.markdown("""
### 1. Improve Awareness

Organizations can improve awareness of available mental-health
resources, benefits and support programs.

### 2. Strengthen Confidentiality

Clear communication about privacy and anonymity may reduce
uncertainty around accessing mental-health support.

### 3. Provide Accessible Support

Companies can make information about counselling and employee
assistance resources easier to find and access.

### 4. Reduce Workplace Barriers

Organizations can review workplace policies and employee support
when mental health is reported as affecting work.

### 5. Monitor Workplace Support

Organizations can periodically evaluate whether employees know
about and can access available mental-health resources.

**Note:** These implications are based on observed associations
in survey data and should not be interpreted as causal effects.
""")


# ============================================================
# DATA LIMITATIONS
# ============================================================

st.header("⚠️ Data Limitations")

st.markdown("""
- The dataset is based on survey responses and may not represent
  the entire technology workforce.

- The data comes from a specific survey period and may not reflect
  current workplace conditions.

- Some demographic and workplace categories contain missing or
  limited responses.

- Treatment rates describe associations between variables and do
  not establish cause-and-effect relationships.

- Geographic comparisons should be interpreted carefully because
  respondent counts vary across countries and states.
""")


# ============================================================
# SUMMARY
# ============================================================

st.header("📋 Summary")

st.write(
    f"""
    This dashboard analyzes mental health treatment-seeking behaviour
    among technology-sector survey respondents.

    After applying the dashboard filters, the analysis contains
    {len(filtered_df):,} respondents, of whom {treatment_count:,}
    reported receiving mental health treatment. This corresponds to
    a treatment rate of {treatment_rate:.1f}%.

    The analysis also examines how treatment rates vary across
    family history, work interference, workplace benefits,
    company size, gender and other workplace factors.

    The results highlight differences in treatment-seeking behaviour
    across several groups while recognizing that the survey data
    shows associations rather than causal relationships.
    """
)


# ============================================================
# CONCLUSION
# ============================================================

st.header("🎯 Conclusion")

st.write("""
Mental health treatment-seeking behaviour varies across demographic
and workplace factors in this survey.

The dashboard helps identify patterns related to family history,
work interference, workplace benefits, company size and other
factors that may be relevant when studying mental-health support
in technology workplaces.

Overall, the analysis can be used as a starting point for
understanding employee experiences and identifying areas where
mental-health awareness, accessibility and workplace support can
be strengthened.

These findings should be interpreted as associations observed in
the survey data rather than evidence of cause and effect.
""")


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

<b>Mental Health in Tech Survey</b><br>

Exploratory Data Analysis Dashboard<br>

Built with Python • Pandas • Matplotlib • Seaborn • Plotly • Streamlit

</div>
""", unsafe_allow_html=True)

# 🧠 Mental Health in Tech Survey

An exploratory data analysis project investigating mental health treatment-seeking behaviour among technology-sector respondents and its relationship with demographic and workplace factors.

## 📊 Live Dashboard

🔗 **Streamlit Dashboard:**
https://mentalhealthsurveyproject-fuwwzrme9vfnbrnzobbbbw.streamlit.app/

---

## 🎯 Project Objective

The objective of this project is to explore patterns in mental health treatment-seeking behaviour among technology professionals.

The analysis focuses on questions such as:

* How many respondents reported receiving mental health treatment?
* How does treatment-seeking vary across demographic groups?
* Is treatment-seeking associated with family history of mental illness?
* How does workplace interference relate to treatment rates?
* How do workplace benefits, care options and anonymity relate to treatment?
* Do treatment rates vary across company sizes and geographic locations?

---

## 📁 Dataset

The project uses the **Mental Health in Tech Survey** dataset.

The dataset contains survey responses covering:

* Demographic information
* Employment details
* Mental health history
* Mental health treatment
* Workplace benefits
* Mental health care options
* Workplace interference
* Company size
* Geographic information

The original survey was conducted among people working in the technology sector.

---

## 🧹 Data Preparation

The following data preparation steps were performed:

* Loaded the dataset using Pandas.
* Restricted age values to a realistic working-age range of **18–65**.
* Standardized gender values into consistent categories.
* Handled missing values in selected workplace-related fields.
* Created a cleaned gender field for analysis.
* Calculated treatment rates across different demographic and workplace groups.
* Applied a minimum respondent threshold of **20 respondents** for country and US-state treatment-rate comparisons to reduce the impact of very small groups.

---

## 📈 Exploratory Data Analysis

The analysis covers several areas:

### Respondent Profile

* Age distribution
* Gender distribution
* Top countries by number of respondents

### Mental Health Treatment

* Overall treatment distribution
* Treatment rate by country
* Treatment rate by US state

### Workplace Factors

* Family history of mental illness
* Gender
* Employer-provided mental health benefits
* Awareness of care options
* Anonymity
* Work interference
* Company size
* Workplace wellness programs

---

## 💡 Key Findings

The dashboard highlights several patterns in the survey data:

* Approximately half of the analyzed respondents reported receiving mental health treatment.
* Treatment rates vary across respondents with and without a family history of mental illness.
* Treatment rates differ across levels of work interference.
* Treatment rates vary across workplace benefit groups.
* Treatment rates differ across company-size categories.
* Geographic treatment rates vary across countries and US states with sufficient respondent counts.

The dashboard allows these patterns to be explored interactively using treatment and gender filters.

---

## 📊 Interactive Dashboard

The Streamlit dashboard includes:

* Interactive sidebar filters
* KPI cards
* Respondent profile visualizations
* Mental health treatment analysis
* Workplace factor analysis
* Geographic comparisons
* Key insights
* Business implications
* Data limitations

🔗 **Open Dashboard:**
https://mentalhealthsurveyproject-fuwwzrme9vfnbrnzobbbbw.streamlit.app/

---

## 🛠️ Tools & Technologies

* **Python**
* **Pandas** — Data cleaning and analysis
* **NumPy** — Numerical operations
* **Matplotlib** — Data visualization
* **Seaborn** — Statistical visualization
* **Plotly** — Interactive visualization
* **Streamlit** — Interactive dashboard

---

## 📂 Project Structure

```text
MentalHealthSurveyProject/
│
├── app.py
├── survey.csv
├── README.md
└── requirements.txt
```

---

## ⚠️ Limitations

* The dataset is based on survey responses and may not represent the entire technology workforce.
* The survey represents a specific period and may not reflect current workplace conditions.
* Some categories contain missing or limited responses.
* Respondent counts vary considerably across countries and states.
* Observed relationships represent associations and should not be interpreted as proof of cause and effect.

---

## 📌 Conclusion

This project demonstrates how exploratory data analysis and interactive visualization can be used to examine mental health treatment-seeking behaviour and workplace factors in survey data.

The Streamlit dashboard provides an interactive way to explore the dataset and identify patterns across demographic, workplace and geographic dimensions.

---

## 👩‍💻 Author

**Keerthi Senthil**

Data Analyst | Python | SQL | Power BI | Excel

🔗 GitHub: https://github.com/KeerthiAnalyst

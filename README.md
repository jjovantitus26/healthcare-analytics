# Healthcare Patient & Operations Analysis

An end-to-end data analytics project analyzing 54,966 patient records across a hospital network to uncover trends in billing, admissions, and operational efficiency.

**Tools:** Python · SQL · Matplotlib · Seaborn · Power BI

---

## Dataset

- **Source:** [Healthcare Dataset by prasad22 on Kaggle](https://www.kaggle.com/datasets/prasad22/healthcare-dataset)
- **Size:** 55,500 records (54,966 after removing duplicates)
- **Period:** May 2019 – May 2024
- **Features:** Patient demographics, medical condition, doctor, hospital, insurance provider, billing amount, admission type, medication, test results

> Download the dataset from Kaggle and place the CSV in the `data/` folder before running the scripts.

---

## Project Structure

```
healthcare-project/
├── data/
│   ├── healthcare_dataset.csv        # Original Kaggle dataset (not uploaded)
│   └── healthcare_clean.csv          # Cleaned dataset (output of Phase 1)
├── charts/                           # Generated chart images
├── healthcare_phase1_cleaning.py     # Data cleaning & feature engineering
├── healthcare_phase2_sql.py          # SQL business analysis
├── healthcare_phase3_charts.py       # Matplotlib visualizations
├── healthcare_dashboard.pbix         # Power BI dashboard
└── README.md
```

---

## Phase 1 — Data Cleaning

- Standardized column names and fixed inconsistent text casing across all fields
- Converted date columns to datetime and removed 534 duplicate rows
- Engineered new features: `length_of_stay`, `age_group`, `admission_yearmonth`, `high_billing` flag
- Flagged negative billing values as data quality issues for review

---

## Phase 2 — SQL Analysis

| # | Question | Finding |
|---|---|---|
| 1 | Overall KPIs | $1.42B total billing, avg stay 15.5 days, avg billing $25,544 |
| 2 | Billing by condition | Obesity highest at $25,804 — Cancer lowest at $25,152 |
| 3 | Stay by age group | Elderly (65+) stay longest at 15.6 days |
| 4 | Insurance providers | All 5 providers cover ~20% of patients each |
| 5 | Test results vs stay | No significant difference — all groups avg 15.5 days |
| 6 | Admission type | Elective admissions have highest avg billing at $25,612 |
| 7 | Busiest doctors | Michael Smith leads with 27 patients treated |
| 8 | Medication by condition | No single medication dominates any condition |
| 9 | Monthly trend | Stable at 900–1,000 admissions/month, no seasonal pattern |
| 10 | High billing segment | Top 25% avg $43,998 vs $19,393 for the bottom 75% |

---

## Phase 3 — Visualizations

Five charts built with Matplotlib and Seaborn covering:
- Average billing by medical condition
- Length of stay by age group
- Admission type — billing and volume comparison
- Patient volume by insurance provider
- Monthly admissions trend (2019–2024)

All charts saved to the `charts/` folder.

---

## Phase 4 — Power BI Dashboard

Interactive dashboard with:
- 5 KPI cards — Total Patients, Avg Billing, Avg Length of Stay, Avg Age, Total Revenue
- Monthly admissions line chart
- Avg billing by condition bar chart
- Insurance provider volume bar chart
- Admission type donut chart
- Year and medical condition slicers for filtering

---

## Key Insights

- **Billing is uniform across conditions** — all 6 conditions fall within $650 of each other, suggesting standardized pricing rather than condition-driven cost variation
- **Elderly patients drive the longest stays** — targeted discharge planning for the 65+ group could improve bed availability
- **Elective admissions cost more than emergency ones** — likely driven by planned, resource-intensive procedures
- **No seasonal admission patterns** — staffing and resource planning can remain flat year-round
- **High billing patients are a distinct segment** — top 25% average more than double the rest, not explained by age or test results alone

---

## How to Run

```bash
pip install pandas numpy matplotlib seaborn

python healthcare_phase1_cleaning.py
python healthcare_phase2_sql.py
python healthcare_phase3_charts.py
```

Open `healthcare_dashboard.pbix` in Power BI Desktop.

---

## Author

**Jovan Titus**
M.S. Computer Science — Illinois Institute of Technology
Aspiring Data Analyst | Python · SQL · Power BI

[LinkedIn](https://linkedin.com/in/jjovantitus) · [GitHub](https://github.com/jjovantitus26)

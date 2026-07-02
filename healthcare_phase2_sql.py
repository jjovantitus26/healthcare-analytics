# Healthcare Data Analysis
# Author: Jovan Titus
# Phase 2: SQL Analysis

import pandas as pd
import sqlite3

# Load clean data
df = pd.read_csv("data/healthcare_clean.csv")
df.drop_duplicates(inplace=True)
print(f"Loaded {len(df):,} rows for analysis")

conn = sqlite3.connect(":memory:")
df.to_sql("patients", conn, index=False, if_exists="replace")

def run_query(title, sql):
    print(f"\n--- {title} ---")
    result = pd.read_sql_query(sql, conn)
    print(result.to_string(index=False))
    return result


# Overall hospital summary
run_query("Overall Summary", """
    SELECT
        COUNT(*)                          AS total_patients,
        ROUND(AVG(age), 1)                AS avg_age,
        ROUND(AVG(billing_amount), 2)     AS avg_billing,
        ROUND(SUM(billing_amount), 2)     AS total_billing,
        ROUND(AVG(length_of_stay), 1)     AS avg_stay_days,
        COUNT(DISTINCT doctor)            AS total_doctors,
        COUNT(DISTINCT hospital)          AS total_hospitals
    FROM patients
""")


# Billing by medical condition
run_query("Billing by Medical Condition", """
    SELECT
        medical_condition,
        COUNT(*)                          AS total_patients,
        ROUND(AVG(billing_amount), 2)     AS avg_billing,
        ROUND(AVG(length_of_stay), 1)     AS avg_stay_days
    FROM patients
    GROUP BY medical_condition
    ORDER BY avg_billing DESC
""")


# Length of stay by age group
run_query("Length of Stay by Age Group", """
    SELECT
        age_group,
        COUNT(*)                          AS total_patients,
        ROUND(AVG(length_of_stay), 1)     AS avg_stay_days,
        ROUND(AVG(billing_amount), 2)     AS avg_billing
    FROM patients
    GROUP BY age_group
    ORDER BY avg_stay_days DESC
""")


# Insurance provider breakdown
run_query("Insurance Provider Analysis", """
    SELECT
        insurance_provider,
        COUNT(*)                                            AS total_patients,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS share_pct,
        ROUND(AVG(billing_amount), 2)                       AS avg_billing,
        ROUND(SUM(billing_amount), 2)                       AS total_billing
    FROM patients
    GROUP BY insurance_provider
    ORDER BY total_patients DESC
""")


# Test results vs length of stay
run_query("Test Results vs Length of Stay", """
    SELECT
        test_results,
        COUNT(*)                          AS total_patients,
        ROUND(AVG(length_of_stay), 1)     AS avg_stay_days,
        ROUND(AVG(billing_amount), 2)     AS avg_billing
    FROM patients
    GROUP BY test_results
    ORDER BY avg_stay_days DESC
""")


# Admission type breakdown
run_query("Admission Type Breakdown", """
    SELECT
        admission_type,
        COUNT(*)                                            AS total_patients,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS share_pct,
        ROUND(AVG(billing_amount), 2)                       AS avg_billing,
        ROUND(AVG(length_of_stay), 1)                       AS avg_stay_days
    FROM patients
    GROUP BY admission_type
    ORDER BY avg_billing DESC
""")


# Top 10 busiest doctors
run_query("Top 10 Busiest Doctors", """
    SELECT
        doctor,
        COUNT(*)                          AS total_patients,
        ROUND(AVG(billing_amount), 2)     AS avg_billing,
        ROUND(AVG(length_of_stay), 1)     AS avg_stay_days,
        COUNT(DISTINCT medical_condition) AS conditions_treated
    FROM patients
    GROUP BY doctor
    ORDER BY total_patients DESC
    LIMIT 10
""")


# Medication usage by condition
run_query("Most Common Medication per Condition", """
    SELECT
        medical_condition,
        medication,
        COUNT(*)                          AS prescriptions,
        ROUND(AVG(billing_amount), 2)     AS avg_billing
    FROM patients
    GROUP BY medical_condition, medication
    ORDER BY medical_condition, prescriptions DESC
""")


# Monthly admissions trend
run_query("Monthly Admissions Trend", """
    SELECT
        admission_yearmonth               AS month,
        COUNT(*)                          AS admissions,
        ROUND(AVG(billing_amount), 2)     AS avg_billing,
        ROUND(AVG(length_of_stay), 1)     AS avg_stay_days
    FROM patients
    GROUP BY admission_yearmonth
    ORDER BY admission_yearmonth
""")


# High billing vs normal billing patient profile
run_query("High Billing vs Normal Billing", """
    SELECT
        CASE WHEN high_billing = 1
             THEN 'High Billing (Top 25%)'
             ELSE 'Normal Billing (Bottom 75%)'
        END                                       AS billing_segment,
        COUNT(*)                                  AS total_patients,
        ROUND(AVG(billing_amount), 2)             AS avg_billing,
        ROUND(AVG(age), 1)                        AS avg_age,
        ROUND(AVG(length_of_stay), 1)             AS avg_stay_days,
        ROUND(AVG(CASE WHEN test_results = 'Abnormal'
              THEN 1.0 ELSE 0 END) * 100, 1)     AS abnormal_test_pct
    FROM patients
    GROUP BY billing_segment
    ORDER BY avg_billing DESC
""")

conn.close()
print("\nDone.")

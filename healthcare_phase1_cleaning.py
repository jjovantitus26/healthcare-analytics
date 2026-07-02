# Healthcare Data Analysis
# Author: Jovan Titus
# Phase 1: Data Cleaning & Feature Engineering

import pandas as pd
import numpy as np
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:.2f}'.format)

# Load the dataset
df = pd.read_csv("data/healthcare_dataset.csv")
print(f"Loaded {len(df):,} rows and {df.shape[1]} columns")
print(f"Missing values: {df.isnull().sum().sum()}")
print(f"Duplicate rows: {df.duplicated().sum()}")


# Standardize column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Fix inconsistent casing in text columns
text_cols = ['name', 'gender', 'blood_type', 'medical_condition',
             'doctor', 'hospital', 'insurance_provider',
             'admission_type', 'medication', 'test_results']

for col in text_cols:
    df[col] = df[col].str.strip().str.title()

# Clean stray commas from hospital names
df['hospital'] = df['hospital'].str.replace(',', '').str.strip()

# Convert dates
df['date_of_admission'] = pd.to_datetime(df['date_of_admission'])
df['discharge_date']    = pd.to_datetime(df['discharge_date'])

print(f"\nDate range: {df['date_of_admission'].min().date()} to {df['date_of_admission'].max().date()}")


# Feature engineering
df['length_of_stay']      = (df['discharge_date'] - df['date_of_admission']).dt.days
df['admission_year']      = df['date_of_admission'].dt.year
df['admission_month']     = df['date_of_admission'].dt.month
df['admission_yearmonth'] = df['date_of_admission'].dt.to_period('M').astype(str)
df['billing_amount']      = df['billing_amount'].round(2)

def age_group(age):
    if age < 18:   return '0-17'
    elif age < 35: return '18-34'
    elif age < 50: return '35-49'
    elif age < 65: return '50-64'
    else:          return '65+'

df['age_group'] = df['age'].apply(age_group)

billing_75 = df['billing_amount'].quantile(0.75)
df['high_billing'] = (df['billing_amount'] >= billing_75).astype(int)

# Remove rows where discharge is before admission
invalid = (df['length_of_stay'] < 0).sum()
if invalid > 0:
    print(f"Removing {invalid} rows with invalid stay duration")
    df = df[df['length_of_stay'] >= 0]


# Summary
print(f"\nCleaned dataset: {len(df):,} rows, {df.shape[1]} columns")
print(f"Avg billing amount : ${df['billing_amount'].mean():,.2f}")
print(f"Avg length of stay : {df['length_of_stay'].mean():.1f} days")
print(f"Age range          : {df['age'].min()} - {df['age'].max()} years")
print(f"Conditions         : {df['medical_condition'].unique()}")

# Export
os.makedirs("data", exist_ok=True)
df.to_csv("data/healthcare_clean.csv", index=False)
print("\nSaved to data/healthcare_clean.csv")

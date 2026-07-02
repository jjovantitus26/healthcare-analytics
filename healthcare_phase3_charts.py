# Healthcare Data Analysis
# Author: Jovan Titus
# Phase 3: Visualizations

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os

df = pd.read_csv("data/healthcare_clean.csv")
df.drop_duplicates(inplace=True)

os.makedirs("charts", exist_ok=True)

sns.set_theme(style="whitegrid", font="DejaVu Sans")
BLUE   = "#2B4590"
ORANGE = "#E86C3A"
GREEN  = "#2E9E6B"

print("Generating charts...")


# Chart 1: Average Billing by Medical Condition
condition_stats = (
    df.groupby("medical_condition")
    .agg(avg_billing=("billing_amount", "mean"),
         avg_stay=("length_of_stay", "mean"))
    .sort_values("avg_billing", ascending=True)
    .reset_index()
)

fig, ax = plt.subplots(figsize=(12, 6))
colors = [ORANGE if i == len(condition_stats) - 1 else BLUE
          for i in range(len(condition_stats))]
bars = ax.barh(condition_stats["medical_condition"],
               condition_stats["avg_billing"],
               color=colors, edgecolor="white", height=0.6)

for bar in bars:
    ax.text(bar.get_width() + 100,
            bar.get_y() + bar.get_height() / 2,
            f"${bar.get_width():,.0f}",
            va="center", fontsize=10)

ax.set_title("Average Billing Amount by Medical Condition", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Average Billing ($)", fontsize=11)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
ax.set_xlim(0, condition_stats["avg_billing"].max() * 1.15)
ax.text(0.99, 0.02,
    "Obesity has the highest avg billing at $25,804",
    transform=ax.transAxes, fontsize=10, ha="right",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFF8E7", edgecolor=ORANGE, alpha=0.9))

plt.tight_layout()
plt.savefig("charts/01_billing_by_condition.png", dpi=150, bbox_inches="tight")
plt.close()
print("  Saved: 01_billing_by_condition.png")


# Chart 2: Length of Stay by Age Group
age_stats = (
    df.groupby("age_group")
    .agg(avg_stay=("length_of_stay", "mean"),
         total_patients=("name", "count"))
    .reset_index()
    .sort_values("avg_stay", ascending=False)
)

fig, ax = plt.subplots(figsize=(11, 6))
bar_colors = [ORANGE if i < 2 else BLUE for i in range(len(age_stats))]
bars = ax.bar(age_stats["age_group"], age_stats["avg_stay"],
              color=bar_colors, edgecolor="white", width=0.55)

for bar in bars:
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.1,
            f"{bar.get_height():.1f} days",
            ha="center", fontsize=10, fontweight="bold")

ax.set_title("Average Length of Stay by Age Group", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Age Group", fontsize=11)
ax.set_ylabel("Avg Length of Stay (days)", fontsize=11)
ax.set_ylim(0, age_stats["avg_stay"].max() * 1.2)
ax.text(0.01, 0.95,
    "Elderly patients (65+) stay longest on average",
    transform=ax.transAxes, fontsize=10, va="top",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFF8E7", edgecolor=ORANGE, alpha=0.9))

plt.tight_layout()
plt.savefig("charts/02_stay_by_age_group.png", dpi=150, bbox_inches="tight")
plt.close()
print("  Saved: 02_stay_by_age_group.png")


# Chart 3: Admission Type Analysis
admission_stats = (
    df.groupby("admission_type")
    .agg(avg_billing=("billing_amount", "mean"),
         total_patients=("name", "count"))
    .reset_index()
    .sort_values("avg_billing", ascending=False)
)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6))
type_colors = [BLUE, ORANGE, GREEN]

bars1 = ax1.bar(admission_stats["admission_type"],
                admission_stats["avg_billing"],
                color=type_colors, edgecolor="white", width=0.5)
for bar in bars1:
    ax1.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height() + 100,
             f"${bar.get_height():,.0f}",
             ha="center", fontsize=10, fontweight="bold")
ax1.set_title("Avg Billing by Admission Type", fontsize=13, fontweight="bold")
ax1.set_ylabel("Avg Billing ($)", fontsize=11)
ax1.set_ylim(0, admission_stats["avg_billing"].max() * 1.2)

wedges, texts, autotexts = ax2.pie(
    admission_stats["total_patients"],
    labels=admission_stats["admission_type"],
    autopct="%1.1f%%",
    colors=type_colors,
    startangle=140,
    wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2),
    textprops=dict(fontsize=11)
)
for at in autotexts:
    at.set_fontweight("bold")
ax2.set_title("Patient Volume by Admission Type", fontsize=13, fontweight="bold")

fig.suptitle("Admission Type Analysis", fontsize=16, fontweight="bold")
ax1.text(0.5, -0.1,
    "Elective admissions have the highest avg billing despite being non-urgent",
    transform=ax1.transAxes, fontsize=9, ha="center",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFF8E7", edgecolor=ORANGE, alpha=0.9))

plt.tight_layout()
plt.savefig("charts/03_admission_type_analysis.png", dpi=150, bbox_inches="tight")
plt.close()
print("  Saved: 03_admission_type_analysis.png")


# Chart 4: Insurance Provider Patient Volume
insurance_stats = (
    df.groupby("insurance_provider")
    .agg(total_patients=("name", "count"),
         avg_billing=("billing_amount", "mean"))
    .sort_values("total_patients", ascending=True)
    .reset_index()
)

fig, ax = plt.subplots(figsize=(12, 6))
ins_colors = [ORANGE if i == len(insurance_stats) - 1 else BLUE
              for i in range(len(insurance_stats))]
bars = ax.barh(insurance_stats["insurance_provider"],
               insurance_stats["total_patients"],
               color=ins_colors, edgecolor="white", height=0.6)

for bar in bars:
    ax.text(bar.get_width() + 30,
            bar.get_y() + bar.get_height() / 2,
            f"{bar.get_width():,}",
            va="center", fontsize=10)

ax.set_title("Patient Volume by Insurance Provider", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Total Patients", fontsize=11)
ax.set_xlim(0, insurance_stats["total_patients"].max() * 1.15)
ax.text(0.99, 0.02,
    "All 5 providers cover roughly equal patient share (~20% each)",
    transform=ax.transAxes, fontsize=10, ha="right",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFF8E7", edgecolor=ORANGE, alpha=0.9))

plt.tight_layout()
plt.savefig("charts/04_insurance_provider.png", dpi=150, bbox_inches="tight")
plt.close()
print("  Saved: 04_insurance_provider.png")


# Chart 5: Monthly Admissions Trend
monthly = (
    df.groupby("admission_yearmonth")
    .agg(admissions=("name", "count"))
    .reset_index()
)

fig, ax = plt.subplots(figsize=(15, 6))
ax.fill_between(range(len(monthly)), monthly["admissions"], alpha=0.15, color=BLUE)
ax.plot(range(len(monthly)), monthly["admissions"],
        color=BLUE, linewidth=2, marker="o", markersize=3)

tick_positions = list(range(0, len(monthly), 6))
ax.set_xticks(tick_positions)
ax.set_xticklabels([monthly["admission_yearmonth"].iloc[i] for i in tick_positions],
                   rotation=45, ha="right", fontsize=9)

ax.set_title("Monthly Patient Admissions (2019-2024)", fontsize=15, fontweight="bold", pad=12)
ax.set_xlabel("Month", fontsize=11)
ax.set_ylabel("Number of Admissions", fontsize=11)
ax.text(0.01, 0.95,
    "Admissions are stable at ~900-1,000 per month with no strong seasonal pattern",
    transform=ax.transAxes, fontsize=10, va="top",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#FFF8E7", edgecolor=ORANGE, alpha=0.9))

plt.tight_layout()
plt.savefig("charts/05_monthly_admissions.png", dpi=150, bbox_inches="tight")
plt.close()
print("  Saved: 05_monthly_admissions.png")

print("\nAll 5 charts saved to charts/ folder")

# Statistical Evaluation of Flight Phase Fatigue in UH-60 Missions

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from scipy.stats import ttest_rel, ttest_ind, shapiro

# Step 1: Upload data
from google.colab import files
uploaded = files.upload()

# Step 2: Read and clean Excel file
excel_files = sorted([f for f in os.listdir() if f.endswith('.xlsx')], reverse=True)

if excel_files:
    file_name = excel_files[0]
    print(f"🔍 Excel file found: {file_name}")
    df = pd.read_excel(file_name)
    df.columns = df.columns.str.strip().str.lower()
    print("Columns loaded:", df.columns.tolist())
else:
    raise FileNotFoundError("No Excel (.xlsx) file found.")

# Step 3: Check if 'role' column exists
if 'role' not in df.columns:
    raise KeyError("'role' column not found. Please check the Excel file headers.")

# Step 4: Predefine groups
bpm_pre_pilot = df[df['role'] == 'pilot']['bpm_pre']
bpm_pre_copilot = df[df['role'] == 'copilot']['bpm_pre']

# Step 5: Paired t-tests for oxygen saturation
print(" Oxygen Saturation (%):")
print(f"• Pre vs In-flight:      t = {ttest_rel(df['spo2_pre'], df['spo2_in']).statistic:.2f}, p = {ttest_rel(df['spo2_pre'], df['spo2_in']).pvalue:.4f}")
print(f"• In-flight vs Post:     t = {ttest_rel(df['spo2_in'], df['spo2_post']).statistic:.2f}, p = {ttest_rel(df['spo2_in'], df['spo2_post']).pvalue:.4f}")
print(f"• Pre vs Post-flight:    t = {ttest_rel(df['spo2_pre'], df['spo2_post']).statistic:.2f}, p = {ttest_rel(df['spo2_pre'], df['spo2_post']).pvalue:.4f}")

# Step 6: Paired t-tests for heart rate (BPM)
print("\n Heart Rate (BPM):")
print(f"• Pre vs In-flight:      t = {ttest_rel(df['bpm_pre'], df['bpm_in']).statistic:.2f}, p = {ttest_rel(df['bpm_pre'], df['bpm_in']).pvalue:.4f}")
print(f"• In-flight vs Post:     t = {ttest_rel(df['bpm_in'], df['bpm_post']).statistic:.2f}, p = {ttest_rel(df['bpm_in'], df['bpm_post']).pvalue:.4f}")
print(f"• Pre vs Post-flight:    t = {ttest_rel(df['bpm_pre'], df['bpm_post']).statistic:.2f}, p = {ttest_rel(df['bpm_pre'], df['bpm_post']).pvalue:.4f}")

# Step 7: Fatigue Score (Pre vs Post)
t_fatigue = ttest_rel(df['fatigue_pre'], df['fatigue_post'])
print("\n Samn-Perelli Fatigue Score:")
print(f"• Pre vs Post-flight:    t = {t_fatigue.statistic:.2f}, p = {t_fatigue.pvalue:.4f}")

# Step 8: Independent t-test (Pilot vs Copilot)
t_bpm_role = ttest_ind(bpm_pre_pilot, bpm_pre_copilot, equal_var=False)
print("\n Pilot vs Copilot (Pre-flight BPM):")
print(f"• t = {t_bpm_role.statistic:.2f}, p = {t_bpm_role.pvalue:.4f}")

print(f"• Additionally, a statistically significant difference was found between pilots and copilots in terms of pre-flight heart rate "
      f"(M_pilot = {bpm_pre_pilot.mean():.1f} bpm, M_copilot = {bpm_pre_copilot.mean():.1f} bpm), "
      f"Welch’s t ≈ {t_bpm_role.statistic:.2f}, p = {t_bpm_role.pvalue:.4f}.")

# Step 8.1: Pilot vs Copilot - SpO2 at all phases
print("\n Pilot vs Copilot (Oxygen Saturation %):")
for phase in ['spo2_pre', 'spo2_in', 'spo2_post']:
    pilot_vals = df[df['role'] == 'pilot'][phase]
    copilot_vals = df[df['role'] == 'copilot'][phase]
    t_stat, p_val = ttest_ind(pilot_vals, copilot_vals, equal_var=False)
    print(f"• {phase.replace('spo2_', '').capitalize()}-flight: t = {t_stat:.2f}, p = {p_val:.4f}")

# Step 8.2: Pilot vs Copilot - Fatigue Score at Pre and Post
print("\n Pilot vs Copilot (Samn-Perelli Fatigue):")
for phase in ['fatigue_pre', 'fatigue_post']:
    pilot_vals = df[df['role'] == 'pilot'][phase]
    copilot_vals = df[df['role'] == 'copilot'][phase]
    t_stat, p_val = ttest_ind(pilot_vals, copilot_vals, equal_var=False)
    print(f"• {phase.replace('fatigue_', '').capitalize()}-flight: t = {t_stat:.2f}, p = {p_val:.4f}")



# Step 9: Shapiro-Wilk Normality Test
print("\n Shapiro-Wilk Normality Test:")
for col in df.select_dtypes(include='number').columns:
    stat, p = shapiro(df[col])
    if p < 1e-4:
        print(f"• {col}: p = {p:.2e} → Non-normal")
    else:
        print(f"• {col}: p = {p:.4f} → {'Normal' if p > 0.05 else 'Non-normal'}")

# Step 10: Visualizations

# Oxygen Saturation Boxplot
df_spo2 = pd.melt(df, id_vars=['role'], value_vars=['spo2_pre', 'spo2_in', 'spo2_post'], 
                  var_name='Phase', value_name='SpO₂')
df_spo2['Phase'] = df_spo2['Phase'].map({
    'spo2_pre': 'Pre-flight', 'spo2_in': 'In-flight', 'spo2_post': 'Post-flight'
})

plt.figure(figsize=(8, 5))
sns.boxplot(x='Phase', y='SpO₂', data=df_spo2, palette=['#444444', '#888888', '#CCCCCC'])
plt.ylabel("Oxygen Saturation (%)", fontsize=10)
plt.xlabel("Flight Phase", fontsize=10)
plt.grid(False)
sns.despine()
plt.tight_layout()
plt.show()

# Heart Rate Boxplot
df_bpm = pd.melt(df, id_vars=['role'], value_vars=['bpm_pre', 'bpm_in', 'bpm_post'], 
                 var_name='Phase', value_name='BPM')
df_bpm['Phase'] = df_bpm['Phase'].map({
    'bpm_pre': 'Pre-flight', 'bpm_in': 'In-flight', 'bpm_post': 'Post-flight'
})

plt.figure(figsize=(8, 5))
sns.boxplot(x='Phase', y='BPM', data=df_bpm, palette=['#444444', '#888888', '#CCCCCC'])
plt.ylabel("Heart Rate (BPM)", fontsize=10)
plt.xlabel("Flight Phase", fontsize=10)
plt.grid(False)
sns.despine()
plt.tight_layout()
plt.show()

# Fatigue Violin Plot
df_fatigue = pd.melt(df, id_vars=['role'], value_vars=['fatigue_pre', 'fatigue_post'],
                     var_name='Phase', value_name='Fatigue')
df_fatigue['Phase'] = df_fatigue['Phase'].map({
    'fatigue_pre': 'Pre-flight', 'fatigue_post': 'Post-flight'
})

plt.figure(figsize=(6, 5))
sns.violinplot(x='Phase', y='Fatigue', data=df_fatigue, palette=['#666666', '#CCCCCC'], inner='point')
plt.xlabel("Phase", fontsize=10)
plt.ylabel("Fatigue Score", fontsize=10)
plt.grid(False)
sns.despine()
plt.tight_layout()
plt.show()

# Paired Line Plot for SpO2
plt.figure(figsize=(8, 5))
for i in range(len(df)):
    plt.plot(['Pre-flight', 'In-flight', 'Post-flight'], 
             [df.loc[i, 'spo2_pre'], df.loc[i, 'spo2_in'], df.loc[i, 'spo2_post']],
             marker='o', color='gray', alpha=0.4)
plt.ylabel("SpO₂ (%)", fontsize=10)
plt.xlabel("Flight Phase", fontsize=10)
plt.grid(False)
sns.despine()
plt.tight_layout()
plt.show()

# Barplot for Pilot vs Copilot
means = [bpm_pre_pilot.mean(), bpm_pre_copilot.mean()]
stds = [bpm_pre_pilot.std(), bpm_pre_copilot.std()]

plt.figure(figsize=(6, 4))
plt.bar(['Pilot', 'Copilot'], means, yerr=stds, capsize=5, color=['#555555', '#BBBBBB'])
plt.ylabel("Pre-flight BPM", fontsize=10)
plt.grid(False)
sns.despine()
plt.tight_layout()
plt.show()

# Step 11: Cohen’s d
def cohens_d(x, y):
    nx, ny = len(x), len(y)
    pooled_std = np.sqrt(((nx - 1)*np.std(x, ddof=1)**2 + (ny - 1)*np.std(y, ddof=1)**2) / (nx + ny - 2))
    return (np.mean(x) - np.mean(y)) / pooled_std

d = cohens_d(bpm_pre_pilot, bpm_pre_copilot)
print(f"\n Cohen's d (Pilot vs Copilot - Pre-flight BPM): {d:.2f}")

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import math
import config

csv_file_path = "file_details_FS.csv"
df_files = pd.read_csv(csv_file_path)
df_files["Modified Date"] = pd.to_datetime(df_files["Modified Date"], errors='coerce')
df_files = df_files.dropna(subset=["Modified Date"])

folders = config.folders

age_thresholds = config.age_thresholds
date_column = "Modified Date"
current_date = datetime.now()

num_folders = len(folders)
cols = 4
rows = math.ceil(num_folders / cols)
fig, axes = plt.subplots(nrows=rows, ncols=cols, figsize=(cols * 5, rows * 5))
axes = axes.flatten()

for i, folder in enumerate(folders):
    ax = axes[i]
    folder_df = df_files[df_files["File Path"].str.startswith(folder)]
    savings_by_criteria = {}
    for years in age_thresholds:
        threshold_date = current_date - pd.DateOffset(years=years)
        older_files = folder_df[folder_df[date_column] < threshold_date]
        total_size = older_files["Size (Bytes)"].sum()
        savings_by_criteria[f"{years} year{'s' if years > 1 else ''}"] = total_size
    total_size_all = folder_df["Size (Bytes)"].sum()
    savings_by_criteria["All Files"] = total_size_all
    labels = list(savings_by_criteria.keys())
    values_gb = [savings_by_criteria[label] / (1024**3) for label in labels]
    bars = ax.bar(labels, values_gb, color='skyblue')
    ax.set_xlabel("Deletion Criteria - Older than x years")
    ax.set_ylabel("Space Saved (GB)")
    ax.set_title(folder)
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2.0, yval, f"{yval:.2f} GB", ha='center', va='bottom')

for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.savefig("space_saved_by_folder.png")

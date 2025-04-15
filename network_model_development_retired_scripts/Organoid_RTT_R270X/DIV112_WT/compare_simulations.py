from netpyne import sim
import os
from datetime import datetime as dt
import json
from RBS_network_models.sim_analysis import process_simulation_v3
from RBS_network_models.Organoid_RTT_R270X.DIV112_WT.src.conv_params import conv_params, mega_params
from RBS_network_models.sensitivity_analysis import prepare_permuted_sim_v2
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Notes ===================================================================================================
# aw 2025-03-14 16:59:36 - compare WT and MUT models for grant thing

wt_data_path = "/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/Organoid_RTT_R270X/DIV112_WT/sensitivity_analyses/2025-03-13_propVelocity_3_slower_propVelocity__data_65s_overrideMUT_2_axes/_propVelocity_3_slower_propVelocity_/_propVelocity_3_slower_propVelocity_/network_data.npy"
mut_data_path = "/pscratch/sd/a/adammwea/workspace/RBS_network_models/data/Organoid_RTT_R270X/DIV112_WT/sensitivity_analyses/2025-03-13_propVelocity_3_slower_propVelocity__data_65s_overrideMUT_2_axes/weightIE_5/weightIE_5/network_data.npy"

# Main ===================================================================================================
# Load data
wt_data = np.load(wt_data_path, allow_pickle=True).item()
mut_data = np.load(mut_data_path, allow_pickle=True).item()

# Extract burst duration and burst amplitude
wt_burst_duration = wt_data['bursting_data']['burst_metrics']['burst_duration']['data']
wt_burst_amplitude = wt_data['bursting_data']['burst_metrics']['burst_amp']['data']
mut_burst_duration = mut_data['bursting_data']['burst_metrics']['burst_duration']['data']
mut_burst_amplitude = mut_data['bursting_data']['burst_metrics']['burst_amp']['data']

# Convert to Pandas DataFrame for visualization
df_burst_duration = pd.DataFrame({
    'Value': np.concatenate([wt_burst_duration, mut_burst_duration]),
    'Model': ['WT'] * len(wt_burst_duration) + ['MUT'] * len(mut_burst_duration)
})

df_burst_amplitude = pd.DataFrame({
    'Value': np.concatenate([wt_burst_amplitude, mut_burst_amplitude]),
    'Model': ['WT'] * len(wt_burst_amplitude) + ['MUT'] * len(mut_burst_amplitude)
})

# Define colors
colors = {"WT": "#85C1E9", "MUT": "#E74C3C"}  # Light blue & pastel red
dot_colors = {"WT": "#2E86C1", "MUT": "#C0392B"}  # Darker shades for scatter points

# Set plot style
sns.set(style="white", font_scale=1.5)

# Create a figure with two subplots (side by side)
fig, axes = plt.subplots(1, 2, figsize=(6, 6), sharey=False, constrained_layout=True)
ax1, ax2 = axes

# Bar plots for burst duration (left Y-axis)
sns.barplot(
    data=df_burst_duration, x="Model", y="Value", ax=ax1, ci="sd",
    capsize=0.1, errwidth=1.5, palette=colors, width=1
)

# Scatter points for burst duration (correctly centered)
sns.stripplot(
    data=df_burst_duration, x="Model", y="Value", ax=ax1,
    hue="Model", palette=dot_colors, jitter=False, dodge=False, size=10, alpha=0.7
)

# Bar plots for burst amplitude (right Y-axis)
sns.barplot(
    data=df_burst_amplitude, x="Model", y="Value", ax=ax2, ci="sd",
    capsize=0.1, errwidth=1.5, palette=colors, width=1
)

# Scatter points for burst amplitude (correctly centered)
sns.stripplot(
    data=df_burst_amplitude, x="Model", y="Value", ax=ax2,
    hue="Model", palette=dot_colors, jitter=False, dodge=False, size=10, alpha=0.7
)

# Set labels and titles
#ax1.set_title("Burst Duration", fontsize=16)
#ax2.set_title("Burst Amplitude", fontsize=16)
#put axis label on the right
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("right")
#ax2.set_title("Burst Amplitude", fontsize=16)

ax1.set_ylabel("Duration (s)", color="black")
ax2.set_ylabel("Amplitude (Hz)", color="black")

# remove x axis label
ax1.set_xlabel("")
ax2.set_xlabel("")


# Remove redundant legends
# ax1.get_legend().remove()
# ax2.get_legend().remove()

# Remove unnecessary spines and grid
sns.despine(ax=ax1, left=False, right=True, bottom=True)
sns.despine(ax=ax2, right=False, left=True, bottom=True)
ax1.grid(axis="y", linestyle="--", alpha=0.5)
ax2.grid(axis="y", linestyle="--", alpha=0.5)

# Save and show plot
plt.savefig("burst_comparison_dual_axis.png", dpi=300)
plt.savefig("burst_comparison_dual_axis.pdf")
#plt.show()

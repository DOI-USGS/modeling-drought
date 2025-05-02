### Import Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from scipy import stats
from scipy import interpolate
from Task_config.defaults import *
from Task_config.functions import *
from Task_config.parameters import *

### Plotting

# make figure
fig_pred_interval = plt.figure(
    1,
    figsize=(
        target_single_plotwidth,
        target_single_plotwidth / aspect_single_plot,
    ),
    gid="figure-" + basename_gid_forecast_summary_1,
)
# add axes for the forecast
ax_pred_interval = fig_pred_interval.add_axes(
    [0.1, 0.15, 0.85, 0.75], gid="axis-" + basename_gid_forecast_summary_1
)

### Data Arrays
# load drought data
drought_data = pd.read_csv("Task_Data/UQ_summaries_for_JeffreyHayley_WDroughtDims.csv")

# load wet data
wet_data = pd.read_csv("Task_Data/UQ_summaries_for_JeffreyHayley_WVeryWetDims.csv")

horizon_weeks = drought_data["horizon_weeks"].to_list()
horizon_weeks.insert(0, 0.0)
avg_width_top = (drought_data["ave_PI_width"] / 1.0).to_list()
avg_width_top.insert(0, 0.0)
# avg_width_bottom = (drought_data["ave_PI_width"] / -2.0).to_list()
# avg_width_bottom.insert(0, 0.0)

ax_pred_interval.fill_between(
    horizon_weeks,
    avg_width_top,
    np.zeros_like(avg_width_top),
    color=median_color_hex,
    linewidth=0.0,
    alpha=0.5,
    label="Median Prediction",
)
for i in range(1, len(horizon_weeks)):
    ax_pred_interval.text(
        horizon_weeks[i],
        avg_width_top[i],
        str(round(avg_width_top[i] * 1.0, 1)) + "%",
        ha="center",
        va="bottom",
    )
    ax_pred_interval.plot(
        [horizon_weeks[i], horizon_weeks[i]],
        [0.0, avg_width_top[i]],
        linestyle=":",
        color="k",
    )
ax_pred_interval.set_xlim(-5, 96)
ax_pred_interval.set_ylim(0, 100)
# ax_pred_interval.set_yticks([-40, -20, 0, 20, 40], ["-40%", "-20%", "0%", "20%", "40%"])
ax_pred_interval.set_yticks(
    [0, 20, 40, 60, 80, 100], ["0%", "20%", "40%", "60%", "80%", "100%"]
)
ax_pred_interval.set_xticks(
    [0, 7, 14, 28, 56, 91],
    [0, 1, 2, 4, 8, 13],
)
ax_pred_interval.set_title(
    "Streamflow Prediction Interval", loc="left", weight="extra bold", color="k"
)
ax_pred_interval.spines["top"].set_visible(False)
ax_pred_interval.spines["right"].set_visible(False)
ax_pred_interval.set_xlabel("Prediction Horizon in Weeks", weight="semibold")
ax_pred_interval.grid(visible=True, axis="y")
ax_pred_interval.set_axisbelow(True)
ax_pred_interval.tick_params(direction="out")

# make svg
fig_pred_interval.savefig("Task2/out/fc_summary.png", dpi=150, metadata=None)
fig_pred_interval.savefig("Task2/out/fc_summary.svg", dpi=150, metadata=None)

# remove metadata
remove_metadata_and_fix("Task2/out/fc_summary.svg", "src/assets/svgs/fc_summary.svg")


# make figure
fig_wd = plt.figure(
    2,
    figsize=(
        target_single_plotwidth,
        target_single_plotwidth / aspect_single_plot,
    ),
    gid="figure-" + basename_gid_forecast_summary_2,
)
# add axes for the forecast
ax_wd = fig_wd.add_axes(
    [0.1, 0.15, 0.85, 0.75], gid="axis-" + basename_gid_forecast_summary_2
)

drought_top = (drought_data["ave_q95_when_obs_drought"]).to_list()
drought_bottom = (drought_data["ave_q05_when_obs_drought"]).to_list()
drought_mid = (drought_data["ave_q50_when_obs_drought"]).to_list()

horizon_weeks = wet_data["horizon_weeks"].to_list()
wet_top = (wet_data["ave_q95_when_obs_verywet"]).to_list()
wet_bottom = (wet_data["ave_q05_when_obs_verywet"]).to_list()
wet_mid = (wet_data["ave_q50_when_obs_verywet"]).to_list()
# horizon_weeks.insert(0, 0.0)
# wet_top.insert(0, 100.0)
# drought_top.insert(0, 20.0)
# drought_bottom.insert(0, 0.0)
# drought_mid.insert(0, 10.0)
# wet_bottom.insert(0, 80.0)
# wet_mid.insert(0, 90.0)

ax_wd.fill_between(
    horizon_weeks,
    drought_top,
    drought_bottom,
    color=lower_color_limit_hex,
    linewidth=0.0,
    alpha=0.15,
    gid="drought-forecast-summary-patch",
)
ax_wd.plot(
    horizon_weeks,
    drought_mid,
    color=lower_color_limit_hex,
    alpha=0.15,
    gid="drought-forecast-summary-line",
)
# ax_wd.plot([0, 0], [0, 20], color="tab:red", linewidth=2)

ax_wd.fill_between(
    horizon_weeks,
    wet_top,
    wet_bottom,
    color=upper_color_limit_hex,
    linewidth=0.0,
    alpha=0.15,
    gid="wet-forecast-summary-patch",
)
ax_wd.plot(
    horizon_weeks,
    wet_mid,
    color=upper_color_limit_hex,
    alpha=0.15,
    gid="wet-forecast-summary-line",
)
# ax_wd.plot([0, 0], [80, 100], color="tab:blue", linewidth=2)

ax_wd.set_xlim(-5, 96)
ax_wd.set_ylim(0, 100)
ax_wd.set_yticks([0, 20, 40, 60, 80, 100], ["0%", "20%", "40%", "60%", "80%", "100%"])
ax_wd.set_xticks(
    [0, 7, 14, 28, 56, 91],
    [0, 1, 2, 4, 8, 13],
)
ax_wd.set_title(
    "Streamflow Predictions (Drought and Wet Periods)",
    loc="left",
    weight="extra bold",
    color="k",
)
ax_wd.spines["top"].set_visible(False)
ax_wd.spines["right"].set_visible(False)
ax_wd.set_xlabel("Prediction Horizon in Weeks", weight="semibold")
ax_wd.grid(visible=True, axis="y")
ax_wd.set_axisbelow(True)
ax_wd.tick_params(direction="out")

# make svg
fig_wd.savefig("Task2/out/fc_wd_summary.svg", metadata=None)

# remove metadata
remove_metadata_and_fix(
    "Task2/out/fc_wd_summary.svg", "src/assets/svgs/fc_wd_summary.svg"
)

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

horizon_weeks = drought_data["horizon_weeks"].to_list()
horizon_weeks.insert(0, 0.0)
avg_width_top = (drought_data["ave_PI_width"] / 2.0).to_list()
avg_width_top.insert(0, 0.0)
avg_width_bottom = (drought_data["ave_PI_width"] / -2.0).to_list()
avg_width_bottom.insert(0, 0.0)

ax_pred_interval.fill_between(
    horizon_weeks,
    avg_width_top,
    avg_width_bottom,
    color=median_color_hex,
    linewidth=0.0,
    alpha=0.25,
)


ax_pred_interval.plot(
    horizon_weeks,
    avg_width_top,
    color=upper_color_limit_hex,
)

ax_pred_interval.plot(
    horizon_weeks,
    avg_width_bottom,
    color=lower_color_limit_hex,
)

ax_pred_interval.plot([0, 7 * 13], [0, 0], color=median_color_hex, alpha=0.75)

ax_pred_interval.text(
    -20,
    0.0,
    "Issue date:\nstreamflow\npercentile\nknown",
    ha="left",
    va="center",
    weight="semibold",
    gid="prediction-width-label-week-" + str(i),
)

ax_pred_interval.text(
    (13 + 8) * 0.5 * 7,
    0.0,
    "Median prediction",
    ha="center",
    va="bottom",
    weight="semibold",
)

ax_pred_interval.text(
    (13 + 8) * 0.5 * 7,
    avg_width_top[-2],
    "Upper prediction",
    ha="center",
    va="top",
    weight="semibold",
)

ax_pred_interval.text(
    (13 + 8) * 0.5 * 7,
    avg_width_bottom[-2],
    "Lower prediction",
    ha="center",
    va="bottom",
    weight="semibold",
)

ax_pred_interval.scatter(0.0, 0.0, s=100, color=ratio_7, marker="s")
for i in range(1, len(horizon_weeks)):
    week_label = str(int(horizon_weeks[i] / 7)) + " weeks"
    # remove "s" for 1 week
    if i == 1:
        week_label = week_label[:-1]

    ax_pred_interval.text(
        horizon_weeks[i],
        35,
        week_label
        + ":\n"
        + r"+/-"
        + str(round(avg_width_top[i] * 1.0, 1))
        + " percentile",
        ha="center",
        va="bottom",
        weight="semibold",
        gid="prediction-width-label-percent-" + str(i),
        alpha=0.0,
    )
    ax_pred_interval.plot(
        [horizon_weeks[i], horizon_weeks[i]],
        [-35, 35],
        linestyle=":",
        color=ratio_7,
    )
    # ax_pred_interval.text(
    #     horizon_weeks[i],
    #     0.0,
    #     week_label,
    #     rotation=90,
    #     ha="right",
    #     va="center",
    #     weight="semibold",
    #     gid="prediction-width-label-week-" + str(i),
    # )

    ax_pred_interval.plot(
        [horizon_weeks[i], horizon_weeks[i]],
        [avg_width_bottom[i], avg_width_top[i]],
        linestyle="-",
        linewidth=2,
        color=ratio_7,
        gid="prediction-width-line-" + str(i),
        alpha=0.0,
    )

    ax_pred_interval.plot(
        [horizon_weeks[i], horizon_weeks[i]],
        [-50, 50],
        linewidth=40,
        color="none",
        alpha=0.0,
        gid="prediction-width-hover-" + str(i),
        zorder=100,
    )
ax_pred_interval.set_xlim(-20, 100)
ax_pred_interval.set_ylim(-50, 50)
# ax_pred_interval.set_yticks([-40, -20, 0, 20, 40], ["-40%", "-20%", "0%", "20%", "40%"])
# ax_pred_interval.set_yticks(
#     [0, 20, 40, 60, 80, 100], ["0%", "20%", "40%", "60%", "80%", "100%"]
# )
# ax_pred_interval.set_xticks(
#     [0, 7, 14, 28, 56, 91],
#     [0, 1, 2, 4, 8, 13],
# )
plt.axis("off")
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
fig_pred_interval.savefig("Task2/out/fc_summary_desktop.svg", dpi=150, metadata=None)

# remove metadata
remove_metadata_and_fix(
    "Task2/out/fc_summary_desktop.svg", "src/assets/svgs/fc_summary_desktop.svg"
)

# to make the mobile version, we first adjust the figure size to a more horizontal aspect
fig_pred_interval.set_size_inches(
    target_plotwidth_in_mobile,
    target_plotwidth_in_mobile / aspect_single_plot,
)

# make svg
fig_pred_interval.savefig("Task2/out/fc_summary_mobile.svg", metadata=None)

# remove metadata
remove_metadata_and_fix(
    "Task2/out/fc_summary_mobile.svg", "src/assets/svgs/fc_summary_mobile.svg"
)

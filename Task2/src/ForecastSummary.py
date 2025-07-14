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

horizon_weeks = drought_data["horizon"].to_list()
horizon_weeks.insert(0, 0.0)
avg_median = (drought_data["overall_ave_q50"]).to_list()

avg_median.insert(0, median_obs)
avg_width_top = (drought_data["overall_ave_q95"]).to_list()
avg_width_top.insert(0, median_obs)
avg_width_bottom = (drought_data["overall_ave_q05"]).to_list()
avg_width_bottom.insert(0, median_obs)

for i in range(1, len(horizon_weeks)):
    ax_pred_interval.fill_between(
        [horizon_weeks[i - 1], horizon_weeks[i]],
        [avg_width_top[i - 1], avg_width_top[i]],
        [avg_width_bottom[i - 1], avg_width_bottom[i]],
        color=median_color_hex,
        linewidth=0.0,
        alpha=0.5 * (len(horizon_weeks) - i) / len(horizon_weeks),
    )


# this function adds a line and a second background line giving the appearance of white outline
def line_outline(x, y, color, w_linewidth):
    ax_pred_interval.plot(
        x,
        y,
        color="w",
        solid_capstyle="round",
        linewidth=w_linewidth,
        zorder=5,
    )
    ax_pred_interval.plot(
        x,
        y,
        color=color,
        solid_capstyle="round",
        linewidth=w_linewidth * 0.4,
        zorder=6,
    )


line_outline(
    horizon_weeks,
    avg_width_top,
    upper_color_limit_hex,
    line_width_summary,
)

line_outline(
    horizon_weeks,
    avg_width_bottom,
    lower_color_limit_hex,
    line_width_summary,
)

line_outline(
    horizon_weeks,
    avg_median,
    median_color_hex,
    line_width_summary,
)

ax_pred_interval.plot(
    [-50, 0],
    [median_obs, median_obs],
    color=observation_color_hex,
    alpha=1.0,
    linewidth=line_width_summary * 0.4,
    solid_capstyle="round",
    zorder=-2,
)


prediction_bump = 2.0
week_bump = 2.0

ax_pred_interval.text(
    0,
    median_obs + prediction_bump,
    "Today",
    ha="right",
    va="bottom",
    fontweight="semibold",
)
ax_pred_interval.text(
    (13) * 0.75 * 7,
    avg_median[-1] + prediction_bump,
    "Median prediction",
    ha="center",
    va="bottom",
    gid="prediction-interval-median-label",
    fontweight="semibold",
)


ax_pred_interval.text(
    (13) * 0.75 * 7,
    avg_width_top[-1] + prediction_bump,
    "Upper prediction",
    ha="center",
    va="bottom",
    fontweight="semibold",
)

ax_pred_interval.text(
    (13) * 0.75 * 7,
    avg_width_bottom[-1] - prediction_bump,
    "Lower prediction",
    ha="center",
    va="top",
    fontweight="semibold",
)


def ordinal(number):
    rounded = int(round(number, 0))
    ones = rounded % 10
    if ones == 1:
        return str(rounded) + "ˢᵗ"
    elif ones == 2:
        return str(rounded) + "ⁿᵈ"
    elif ones == 3:
        return str(rounded) + "ʳᵈ"
    else:
        return str(rounded) + "ᵗʰ"


ax_pred_interval.scatter(0.0, median_obs, s=100, color=ratio_7, marker="s", zorder=10)
for i in range(1, len(horizon_weeks)):
    week_label = str(int(horizon_weeks[i] / 7)) + " weeks"
    # remove "s" for 1 week
    if i == 1:
        week_label = week_label[:-1]

    ax_pred_interval.text(
        horizon_weeks[i],
        100 - prediction_bump,
        week_label + " out",
        ha="center",
        va="top",
        gid="prediction-width-label-week-" + str(i),
        alpha=0.0,
        zorder=11,
        fontweight="normal",
    )
    ax_pred_interval.text(
        horizon_weeks[i] + week_bump,
        avg_width_top[i] - prediction_bump,
        ordinal(avg_width_top[i]) + " pct",
        ha="left",
        va="top",
        gid="prediction-width-label-upper-percentile-" + str(i),
        alpha=0.0,
        zorder=101,
        fontweight="normal",
    )
    ax_pred_interval.text(
        horizon_weeks[i] + week_bump,
        avg_width_bottom[i] + prediction_bump,
        ordinal(avg_width_bottom[i]) + " pct",
        ha="left",
        va="bottom",
        gid="prediction-width-label-lower-percentile-" + str(i),
        alpha=0.0,
        zorder=101,
        fontweight="normal",
    )

    ax_pred_interval.plot(
        [horizon_weeks[i], horizon_weeks[i]],
        [avg_width_bottom[i], avg_width_top[i]],
        linestyle=":",
        solid_capstyle="round",
        color=ratio_3,
    )

    ax_pred_interval.plot(
        [horizon_weeks[i], horizon_weeks[i]],
        [avg_width_bottom[i], avg_width_top[i]],
        linestyle="-",
        linewidth=line_width_summary * 0.4,
        color=ratio_5,
        gid="prediction-width-line-" + str(i),
        alpha=0.0,
        solid_capstyle="round",
    )

    ax_pred_interval.plot(
        [
            0.5 * (horizon_weeks[i] + horizon_weeks[i - 1]),
            0.5 * (horizon_weeks[i] + horizon_weeks[i - 1]),
        ],
        [0, 100],
        linewidth=35,
        color="none",
        alpha=0.0,
        gid="prediction-width-hover-" + str(i),
        zorder=100,
    )
ax_pred_interval.set_xlim(-20, 100)
ax_pred_interval.set_ylim(0, 100)
ax_pred_interval.set_yticks(
    [0.0, 20.0, 40.0, 60.0, 80.0, 100],
    [
        "0ᵗʰ",
        "20ᵗʰ",
        "40ᵗʰ",
        "60ᵗʰ",
        "80ᵗʰ",
        "100ᵗʰ",
    ],
)
ax_pred_interval.set_xticks(np.linspace(0, 13 * 7, 14), [str(i) for i in range(0, 14)])
ax_pred_interval.set_title(
    "Streamflow prediction interval", loc="left", weight="extra bold", color="k"
)
ax_pred_interval.spines["top"].set_visible(False)
ax_pred_interval.spines["right"].set_visible(False)
ax_pred_interval.set_xlabel("Forecast horizon in weeks", weight="semibold")
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

# to make the tablet version, we first adjust the figure size to a more horizontal aspect
fig_pred_interval.set_size_inches(
    target_plotwidth_in_tablet,
    target_plotwidth_in_tablet / aspect_single_plot,
)

# make svg
fig_pred_interval.savefig("Task2/out/fc_summary_tablet.svg", metadata=None)

# remove metadata
remove_metadata_and_fix(
    "Task2/out/fc_summary_tablet.svg", "src/assets/svgs/fc_summary_tablet.svg"
)

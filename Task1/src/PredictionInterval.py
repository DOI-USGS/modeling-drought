import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy import stats
from scipy import interpolate
from Task_config.defaults import *
from Task_config.functions import *
from Task_config.parameters import *

### Plotting

# make figure
fig = plt.figure(
    1,
    figsize=(target_plotwidth_in_mobile, target_plotwidth_in_mobile / aspect_mobile),
    gid="figure-" + basename_gid_pi,
)

# add axes
ax_LF = fig.add_axes([0.125, 0.575, 0.825, 0.375], gid="axis-" + basename_gid_pi + "1")
ax_forecast = fig.add_axes(
    [0.125, 0.075, 0.825, 0.375], gid="axis-" + basename_gid_pi + "2"
)

### Data Arrays

# loss function x-array
x_LF = np.array([-1.0, 0.0, 1.0])

# load date data
x_forecast = forecast_data["datetime"].values.astype("datetime64[D]")

# load observed data
y_training = forecast_data["observed"]

# load model data (lower, median, and upper)
y_forecast_lower = forecast_format(forecast_data["lower"])
y_forecast_median = forecast_format(forecast_data["median"])
y_forecast_upper = forecast_format(forecast_data["upper"])

# get temporal bounds
lower_bound = np.argmin(np.abs(x_forecast - np.datetime64(date_range[0])))
upper_bound = np.argmin(np.abs(x_forecast - np.datetime64(date_range[1]))) + 1

# generate lines based on percentile
pi_list = [0.05, 0.125, 0.25]
facecolor_list = [(0.9, 0.9, 0.9), (0.75, 0.75, 0.75), (0.5, 0.5, 0.5)]
lower_limit_pi = []
inside_proportion = []
for i, lower_percentile in enumerate(pi_list):

    upper_percentile = 1.0 - lower_percentile
    # Add Popup loss function lines
    ax_LF.plot(
        x_LF,
        pinball_LF(x_LF, 0.0, lower_percentile),
        color=lower_color_limit_hex,
        alpha=0.0,
        zorder=2,
        gid="LF-LOWER-" + str(i),
    )
    ax_LF.plot(
        x_LF,
        pinball_LF(x_LF, 0.0, upper_percentile),
        color=upper_color_limit_hex,
        alpha=0.0,
        zorder=2,
        gid="LF-UPPER-" + str(i),
    )

    # calculate the corresponding z value
    z_val_lower = stats.laplace_asymmetric.ppf(
        lower_percentile, kappa=kappa, loc=loc, scale=scale
    )
    z_val_upper = stats.laplace_asymmetric.ppf(
        upper_percentile, kappa=kappa, loc=loc, scale=scale
    )
    # calculate the forecast line
    if lower_percentile < 0.50:
        y_forecast_temp_lower = y_forecast_median + (
            y_forecast_lower - y_forecast_median
        ) * (z_val_lower - z_median) / (z_val_min - z_median)
    else:
        y_forecast_temp_lower = y_forecast_median + (
            y_forecast_upper - y_forecast_median
        ) * (z_val_lower - z_median) / (z_val_max - z_median)

    if upper_percentile < 0.50:
        y_forecast_temp_upper = y_forecast_median + (
            y_forecast_lower - y_forecast_median
        ) * (z_val_upper - z_median) / (z_val_min - z_median)
    else:
        y_forecast_temp_upper = y_forecast_median + (
            y_forecast_upper - y_forecast_median
        ) * (z_val_upper - z_median) / (z_val_max - z_median)

    # plot the forecast line
    ax_forecast.fill_between(
        x_forecast,
        y_forecast_temp_lower,
        y_forecast_temp_upper,
        color=facecolor_list[i],
        gid="PI-PATCH-" + str(i),
        alpha=0.00001,
        edgecolor="none",
        zorder=0,
    )
    ax_forecast.plot(
        x_forecast,
        y_forecast_temp_lower,
        color=lower_color_limit_hex,
        gid="PI-PATCH-LOWER-" + str(i),
        alpha=0.0,
        zorder=0,
    )
    ax_forecast.plot(
        x_forecast,
        y_forecast_temp_upper,
        color=upper_color_limit_hex,
        gid="PI-PATCH-UPPER-" + str(i),
        alpha=0.0,
        zorder=0,
    )

    # get coordiante of upper bounds at x_max limit
    lower_interp = interpolate.interp1d(
        x_forecast.astype(float), y_forecast_temp_lower, kind="linear"
    )
    lower_limit_pi += [
        lower_interp(np.datetime64(date_range[-1]).astype(float)) / 100.0
    ]

    # calculate what's inside
    inside_count = 0
    count = 0
    outside_count = 0

    # locate where the observation is outside the prediction interval
    missed_x = []
    missed_y = []
    for j in range(lower_bound, upper_bound):
        if (
            y_forecast_temp_lower.values[j] <= y_training.values[j]
            and y_training.values[j] <= y_forecast_temp_upper.values[j]
        ):
            inside_count += 1
        else:
            outside_count += 1
            missed_x += [j]
            missed_y += [y_training.values[j]]
        count += 1

    inside_proportion += [float(inside_count) / float(count)]

    ax_forecast.plot(
        x_forecast[missed_x],
        missed_y,
        clip_on=False,
        markersize=missed_marker_size + float(i / 200),
        alpha=0.0,
        marker="o",
        color=ratio_7,
        markerfacecolor="none",
        linestyle="none",
        gid="PI-missed-" + str(i),
        zorder=3,
    )

for i, pi in enumerate(pi_list):

    popup_text(
        ax_forecast,
        0.6,
        0.7,
        "PI Contains\n"
        + str(round(inside_proportion[i] * 100.0, 1))
        + "% of Observations",
        observation_color_hex,
        "NULL",
        "NULL",
        "center",
        "center",
        "TAG-" + str(i) + "-LABEL",
    )

### Loss Function Plot
# Add static loss function lines
ax_LF.plot(
    x_LF,
    pinball_LF(x_LF, 0.0, 0.5),
    color=median_color_hex,
    zorder=0,
    alpha=0.0,
    gid="LF-LOWER-MEDIAN",
)
# loss function axis parameters
ax_LF.tick_params(direction="out")
ax_LF.set_ylim(0, 1)
ax_LF.set_xlim(-1, 1)
ax_LF.set_xticks(x_LF, ["Lower", "Median", "Upper"], weight="light")
ax_LF.get_yaxis().set_ticks(
    [0, 0.5, 1.0],
    ["Less\nPenalty\n", "", "More\nPenalty"],
    weight="light",
)
ax_LF.set_xlabel("Estimate", weight="semibold")
ax_LF.set_title("Loss Function", loc="left", color="k", weight="extra bold")
ax_LF.spines["top"].set_visible(False)
ax_LF.spines["right"].set_visible(False)
ax_LF.spines["bottom"].set_color(ratio_3)
ax_LF.spines["left"].set_color(ratio_3)
ax_LF.tick_params(axis="both", colors=ratio_3, labelcolor=ratio_5)

### Forecast Plot
# # add static forecast lines
ax_forecast.plot(
    x_forecast,
    y_forecast_median,
    color=median_color_hex,
    gid="PI-PATCH-MEDIAN",
    alpha=0.0,
)
# # add popup forecast lines
obs_forecast = ax_forecast.plot(
    x_forecast,
    y_training,
    color=observation_color_hex,
    linestyle=obs_linestyle,
    alpha=1.0,
    gid="OBSERVED-FORECAST-LINE",
    zorder=2,
    label="Observations",
)
# # dummy missed observations
missed_forecast = ax_forecast.plot(
    [0, 1],
    [1, 1],
    markersize=missed_marker_size - 1.0 / 200.0,
    marker="o",
    color=ratio_7,
    markerfacecolor="none",
    linestyle="none",
    gid="PI-missed-dummy",
    label="Missed Prediction",
)

# forecast axis parameters
ax_forecast.grid(visible=True, axis="y", clip_on=False)
legend = ax_forecast.legend(
    loc="upper left", edgecolor="none", facecolor="none", ncols=2
)
legend.set(gid="legend-pi")
ax_forecast.add_artist(legend)

ax_forecast.tick_params(direction="out")
ax_forecast.set_ylim(0, 100.0)
ax_forecast.set_xlim(np.datetime64(date_range[0]), np.datetime64(date_range[-1]))
start_year = 1971 + np.datetime64(date_range[0], "Y").astype(int)
end_year = 1971 + np.datetime64(date_range[-1], "Y").astype(int)
x_ticks = [np.datetime64(str(i) + "-01-01") for i in range(start_year, end_year)]
x_ticks_labels = [i for i in range(start_year, end_year)]
ax_forecast.set_xticks(x_ticks, x_ticks_labels, weight="light")
ax_forecast.set_yticks(
    [0, 20, 40, 60, 80, 100],
    ["0%", "20%", "40%", "60%", "80%", "100%"],
    weight="light",
)
ax_forecast.set_xlabel("Date", weight="semibold")
ax_forecast.set_title(
    "Streamflow Percentile",
    loc="left",
    color="k",
    weight="extra bold",
)
ax_forecast.spines["top"].set_visible(False)
ax_forecast.spines["right"].set_visible(False)
ax_forecast.tick_params(axis="both", colors=ratio_3, labelcolor=ratio_5)
ax_forecast.set_axisbelow(True)

# river label
plt.figtext(1, 0, river_label, ha="right", va="bottom", alpha=0.5)

# make svg
fig.savefig("Task1/out/pi_example_mobile.svg", dpi=96, metadata=None)

# remove metadata
remove_metadata(
    "Task1/out/pi_example_mobile.svg", "src/assets/svgs/pi_example_mobile.svg"
)

# to make the desktop version, we first adjust the figure size to a more horizontal aspect
fig.set_size_inches(
    target_plotwidth_in_desktop, target_plotwidth_in_desktop / aspect_desktop
)

# we then set a new position for the loss function plot and make it more square
ax_LF.set_position([0.125 / 2.0, 0.075 * 2.0, 0.825 / 3.0, 0.375 * 2.0])
# last we stretch the forecase plot to make it wider
ax_forecast.set_position(
    [0.125 / 2.0 + 1.0 / 3.0, 0.075 * 2.0, 0.825 * 2.0 / 3.0, 0.375 * 2.0]
)
# make svg
fig.savefig("Task1/out/pi_example_desktop.svg", dpi=96, metadata=None)

# remove metadata
remove_metadata(
    "Task1/out/pi_example_desktop.svg", "src/assets/svgs/pi_example_desktop.svg"
)

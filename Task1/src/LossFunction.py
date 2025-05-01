### Import Libraries
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
    figsize=(
        target_plotwidth_in_tablet,
        target_plotwidth_in_tablet / aspect_double_plot_tablet,
    ),
    gid="figure-" + basename_gid_lf,
)
# add axes for loss function
ax_LF = fig.add_axes([0.125, 0.575, 0.825, 0.375], gid="axis-" + basename_gid_lf + "1")
# add axes for the forecast
ax_forecast = fig.add_axes(
    [0.125, 0.075, 0.825, 0.375], gid="axis-" + basename_gid_lf + "2"
)

### Data Arrays

# loss function x-array
x_LF = np.array([-1.0, 0.0, 1.0])

# load date data
x_forecast_raw = forecast_data["datetime"].values.astype("datetime64[D]")

# get temporal bounds
lower_bound = np.argmin(np.abs(x_forecast_raw - np.datetime64(date_range[0])))
upper_bound = np.argmin(np.abs(x_forecast_raw - np.datetime64(date_range[1]))) + 1

# cut data
x_forecast = x_forecast_raw[lower_bound:upper_bound]

# load observed data
y_training = forecast_data["observed"][lower_bound:upper_bound]

# load model data (lower, median, and upper)
y_forecast_lower = forecast_format(forecast_data["lower"][lower_bound:upper_bound])
y_forecast_median = forecast_format(forecast_data["median"][lower_bound:upper_bound])
y_forecast_upper = forecast_format(forecast_data["upper"][lower_bound:upper_bound])

# generate lines based on percentile
for i, percentile in enumerate(
    np.linspace(min_percentile, 1.0 - min_percentile, number_of_frames_lf)
):

    # plot the loss function
    ax_LF.plot(
        x_LF,
        pinball_LF(x_LF, 0.0, percentile),
        color=LFCMap(adjust(percentile)),
        gid="LF-" + str(i),
        alpha=0.0,
        zorder=5,
    )

    # calculate the corresponding z value
    z_val = stats.laplace_asymmetric.ppf(percentile, kappa=kappa, loc=loc, scale=scale)

    # calculate the forecast line
    if percentile < 0.50:
        y_forecast_temp = y_forecast_median + (y_forecast_lower - y_forecast_median) * (
            z_val - z_median
        ) / (z_val_min - z_median)
    else:
        y_forecast_temp = y_forecast_median + (y_forecast_upper - y_forecast_median) * (
            z_val - z_median
        ) / (z_val_max - z_median)

    # plot the forecast line
    ax_forecast.plot(
        x_forecast,
        y_forecast_temp,
        color=LFCMap(adjust(percentile)),
        gid="FORECAST-" + str(i),
        alpha=0.0,
        zorder=5,
    )

# annotations
annotation_instructions = ax_LF.annotate(
    "Tap in the\ngray region",
    color=ratio_5,
    va="center",
    ha="center",
    xy=(-0.8, 0.1),
    xytext=(-0.1, 0.65),
    arrowprops=dict(
        facecolor=ratio_5,
        edgecolor=ratio_5,
        gid="annotation_lossfunction_arrow",
        arrowstyle="fancy",
        connectionstyle="arc3,rad=0.3",
        alpha=1.0,
    ),
    zorder=10,
    gid="annotation_lossfunction",
)

### Loss Function Plot
# Add static loss function lines
ax_LF.plot(
    x_LF,
    pinball_LF(x_LF, 0.0, min_percentile),
    color=np.array(lower_color_limit) / 256.0,
    linestyle="--",
    alpha=static_alpha,
)
ax_LF.plot(
    x_LF,
    pinball_LF(x_LF, 0.0, 0.5),
    color=median_color_hex,
    zorder=0,
    linestyle="--",
    alpha=static_alpha,
)
ax_LF.plot(
    x_LF,
    pinball_LF(x_LF, 0.0, 1.0 - min_percentile),
    color=np.array(upper_color_limit) / 256.0,
    linestyle="--",
    alpha=static_alpha,
)
# Fill between the lower and upper bounds
ax_LF.fill_between(
    x_LF,
    pinball_LF(x_LF, 0.0, min_percentile),
    pinball_LF(x_LF, 0.0, 1.0 - min_percentile),
    color="tab:gray",
    alpha=fill_alpha,
    edgecolor="none",
)
# Add popup loss function lines
ax_LF.plot(
    x_LF,
    pinball_LF(x_LF, 0.0, min_percentile),
    color=np.array(lower_color_limit) / 256.0,
    alpha=0.0,
    zorder=2,
    gid="LOWER-LF-LINE",
)
ax_LF.plot(
    x_LF,
    pinball_LF(x_LF, 0.0, 0.5),
    color=median_color_hex,
    alpha=0.0,
    zorder=2,
    gid="MEDIAN-LF-LINE",
)
ax_LF.plot(
    x_LF,
    pinball_LF(x_LF, 0.0, 1.0 - min_percentile),
    color=np.array(upper_color_limit) / 256.0,
    alpha=0.0,
    zorder=2,
    gid="UPPER-LF-LINE",
)

# loss function axis parameters
ax_LF.tick_params(direction="out")
ax_LF.set_ylim(0, 1)
ax_LF.set_xlim(-1, 1)
ax_LF.set_xticks(x_LF, ["Lower", "Median", "Upper"])
ax_LF.set_yticks([0, 0.5, 1.0], ["Less\nPenalty\n", "", "More\nPenalty"])
ax_LF.set_xlabel("Estimate", weight="semibold")
ax_LF.set_title("Loss Function", loc="left", weight="extra bold", color="k")
ax_LF.spines["top"].set_visible(False)
ax_LF.spines["right"].set_visible(False)
### Forecast Plot
# add static forecast lines
ax_forecast.plot(
    x_forecast,
    y_forecast_lower,
    color=np.array(lower_color_limit) / 256.0,
    linestyle="--",
    alpha=static_alpha,
)
ax_forecast.plot(
    x_forecast,
    y_forecast_median,
    color=median_color_hex,
    linestyle="--",
    alpha=static_alpha,
)
ax_forecast.plot(
    x_forecast,
    y_forecast_upper,
    color=np.array(upper_color_limit) / 256.0,
    linestyle="--",
    alpha=static_alpha,
)
# fill between upper and lower
ax_forecast.fill_between(
    x_forecast,
    y_forecast_lower,
    y_forecast_upper,
    color="tab:gray",
    alpha=fill_alpha,
    edgecolor="none",
)
# add popup forecast lines
ax_forecast.plot(
    x_forecast,
    y_training,
    color=observation_color_hex,
    linestyle=obs_linestyle,
    alpha=0.0,
    gid="observation-full-lf",
)
ax_forecast.plot(
    x_forecast,
    y_forecast_lower,
    color=np.array(lower_color_limit) / 256.0,
    alpha=0.0,
    zorder=2,
    gid="LOWER-FORECAST-LINE",
)
ax_forecast.plot(
    x_forecast,
    y_forecast_median,
    color=median_color_hex,
    alpha=0.0,
    zorder=2,
    gid="MEDIAN-FORECAST-LINE",
)
ax_forecast.plot(
    x_forecast,
    y_forecast_upper,
    color=np.array(upper_color_limit) / 256.0,
    alpha=0.0,
    zorder=2,
    gid="UPPER-FORECAST-LINE",
)

# forecast axis parameters
ax_forecast.grid(visible=True, axis="y", clip_on=False)
ax_forecast.tick_params(direction="out")
ax_forecast.set_ylim(0, 100.0)
ax_forecast.set_xlim(np.datetime64(date_range[0]), np.datetime64(date_range[-1]))
start_year = 1971 + np.datetime64(date_range[0], "Y").astype(int)
end_year = 1971 + np.datetime64(date_range[-1], "Y").astype(int)
x_ticks = [np.datetime64(str(i) + "-01-01") for i in range(start_year, end_year)]
x_ticks_labels = [i for i in range(start_year, end_year)]
ax_forecast.set_xticks(x_ticks, x_ticks_labels)
ax_forecast.set_yticks(
    [0, 20, 40, 60, 80, 100],
    ["0%", "20%", "40%", "60%", "80%", "100%"],
)
ax_forecast.set_xlabel("Date", weight="semibold")
ax_forecast.set_title(
    "Streamflow Percentile", loc="left", weight="extra bold", color="k"
)
ax_forecast.spines["top"].set_visible(False)
ax_forecast.spines["right"].set_visible(False)
ax_forecast.set_axisbelow(True)

# river label
plt.figtext(1, 0, river_label, ha="right", va="bottom", alpha=0.5)

# make svg
fig.savefig("Task1/out/lf_example_tablet.svg", metadata=None)

# remove metadata
remove_metadata_and_fix(
    "Task1/out/lf_example_tablet.svg", "src/assets/svgs/lf_example_tablet.svg"
)

# to make the desktop version, we first adjust the figure size to a more horizontal aspect
fig.set_size_inches(
    target_plotwidth_in_desktop,
    target_plotwidth_in_desktop / aspect_double_plot_desktop,
)

# we then set a new position for the loss function plot and make it more square
ax_LF.set_position([0.125 / 2.0, 0.075 * 2.0, 0.825 / 3.0, 0.375 * 2.0])
# last we stretch the forecase plot to make it wider
ax_forecast.set_position(
    [0.125 / 2.0 + 1.0 / 3.0, 0.075 * 2.0, 0.825 * 2.0 / 3.0, 0.375 * 2.0]
)
annotation_instructions.set_text("Drag mouse over\ngray region")
# make svg
fig.savefig("Task1/out/lf_example_desktop.svg", metadata=None)

# remove metadata
remove_metadata_and_fix(
    "Task1/out/lf_example_desktop.svg", "src/assets/svgs/lf_example_desktop.svg"
)

# to make the mobile version, we first adjust the figure size to a more horizontal aspect
fig.set_size_inches(
    target_plotwidth_in_mobile,
    target_plotwidth_in_mobile / aspect_double_plot_mobile,
)

# we then set a new position for the loss function plot and make it more square
ax_LF.set_position([0.14, 0.6, 0.8, 0.333])
# last we stretch the forecase plot to make it wider
ax_forecast.set_position([0.14, 0.1, 0.8, 0.333])

annotation_instructions.set_text("Tap in the\ngray region")

# make svg
fig.savefig("Task1/out/lf_example_mobile.svg", metadata=None)

# remove metadata
remove_metadata_and_fix(
    "Task1/out/lf_example_mobile.svg", "src/assets/svgs/lf_example_mobile.svg"
)

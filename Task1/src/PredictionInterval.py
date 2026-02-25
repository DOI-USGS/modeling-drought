import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy import stats
from scipy import interpolate
import pyarrow.feather as feather
from Task_config.functions import (
    forecast_format,
    laplace,
    pinball_LF,
    popup_text,
    set_axis_up,
    save_desktop_mobile_tablet,
)
from Task_config.setup_matplotlib import (
    target_plotwidth_in_desktop,
    target_plotwidth_in_mobile,
    target_plotwidth_in_tablet,
    LFCMap,
)

# load in parameters
aspect_double_plot_desktop = snakemake.params["aspect_double_plot_desktop"]
aspect_double_plot_tablet = snakemake.params["aspect_double_plot_tablet"]
aspect_double_plot_mobile = snakemake.params["aspect_double_plot_mobile"]
ratio_7 = snakemake.params["ratio_7"]
lower_color_limit_hex = snakemake.params["lower_color_limit_hex"]
median_color_hex = snakemake.params["median_color_hex"]
upper_color_limit_hex = snakemake.params["upper_color_limit_hex"]
observation_color_hex = snakemake.params["observation_color_hex"]

basename_gid_pi = snakemake.params["basename_gid_pi"]
date_range = snakemake.params["date_range"]
label_year = snakemake.params["label_year"]
year_label_offset = snakemake.params["year_label_offset"]
min_percentile = snakemake.params["min_percentile"]
number_of_frames_lf = snakemake.params["number_of_frames_lf"]
static_alpha = snakemake.params["static_alpha"]
fill_alpha = snakemake.params["fill_alpha"]
loc = snakemake.params["loc"]
scale = snakemake.params["scale"]
kappa = snakemake.params["kappa"]

missed_marker_size = snakemake.params["missed_marker_size"]

# forecast data, contains 90th PI
forecast_data_site = feather.read_feather(snakemake.input[0])
forecast_data = forecast_data_site[forecast_data_site["nday_forecast"] == 7.0]

# 50th PI
forecast_data_50PI_site = feather.read_feather(snakemake.input[1])
forecast_data_50PI = forecast_data_50PI_site[forecast_data_50PI_site["nday_forecast"] == 7.0]

# 75th PI
forecast_data_75PI_site = feather.read_feather(snakemake.input[2])
forecast_data_75PI = forecast_data_75PI_site[forecast_data_75PI_site["nday_forecast"] == 7.0]

# asymmetric laplace distribution
z_val_min, z_val_max, z_median, x_LF = laplace(loc, scale, kappa, min_percentile)

### Plotting

# make figure
fig = plt.figure(
    1,
    figsize=(
        target_plotwidth_in_desktop,
        target_plotwidth_in_desktop / aspect_double_plot_desktop,
    ),
    gid="figure-" + basename_gid_pi,
)

# add axes
ax_LF = fig.add_axes(
    [0.125 / 2.0, 0.075 * 2.0, 0.825 / 3.0, 0.375 * 2.0],
    gid="axis-" + basename_gid_pi + "1",
)
ax_forecast = fig.add_axes(
    [0.125 / 2.0 + 1.0 / 3.0, 0.075 * 2.0, 0.825 * 2.0 / 3.0, 0.375 * 2.0],
    gid="axis-" + basename_gid_pi + "2",
)

### Data Arrays

# load date data
x_forecast = forecast_data["datetime"].values.astype("datetime64[D]")
x_forecast_50PI = forecast_data_50PI["datetime"].values.astype("datetime64[D]")
x_forecast_75PI = forecast_data_75PI["datetime"].values.astype("datetime64[D]")

# load observed data
y_training = forecast_data["observation"]

# load model data (lower, median, and upper)
y_forecast_lower = forecast_format(forecast_data["lower"])
y_forecast_median = forecast_format(forecast_data["median"])
y_forecast_upper = forecast_format(forecast_data["upper"])

# load model data for 50th and 75th percentile
y_forecast_50PI_lower = forecast_format(forecast_data_50PI["50_lower"])
y_forecast_75PI_lower = forecast_format(forecast_data_75PI["75_lower"])
y_forecast_50PI_upper = forecast_format(forecast_data_50PI["50_upper"])
y_forecast_75PI_upper = forecast_format(forecast_data_75PI["75_upper"])

# get temporal bounds
lower_bound = np.argmin(np.abs(x_forecast - np.datetime64(date_range[0])))
upper_bound = np.argmin(np.abs(x_forecast - np.datetime64(date_range[1]))) + 1

# generate lines based on percentile
pi_list = [0.05, 0.125, 0.25]
x_list = [x_forecast,x_forecast_75PI,x_forecast_50PI]
lower_list = [y_forecast_lower, y_forecast_75PI_lower, y_forecast_50PI_lower]
upper_list = [y_forecast_upper, y_forecast_75PI_upper, y_forecast_50PI_upper]
facecolor_list = [(0.9, 0.9, 0.9), (0.75, 0.75, 0.75), (0.5, 0.5, 0.5)]
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


    x_forecast_temp = x_list[i]
    # calculate the forecast line
    if lower_percentile < 0.50:
        y_forecast_temp_lower = lower_list[i]
    else:
        y_forecast_temp_lower = upper_list[i]

    if upper_percentile < 0.50:
        y_forecast_temp_upper = lower_list[i]
    else:
        y_forecast_temp_upper = upper_list[i]

    # plot the forecast line
    ax_forecast.fill_between(
        x_forecast_temp,
        y_forecast_temp_lower,
        y_forecast_temp_upper,
        color=facecolor_list[i],
        gid="PI-PATCH-" + str(i),
        alpha=0.00001,
        edgecolor="none",
        zorder=0,
    )
    ax_forecast.plot(
        x_forecast_temp,
        y_forecast_temp_lower,
        color=lower_color_limit_hex,
        gid="PI-PATCH-LOWER-" + str(i),
        alpha=0.0,
        zorder=0,
    )
    ax_forecast.plot(
        x_forecast_temp,
        y_forecast_temp_upper,
        color=upper_color_limit_hex,
        gid="PI-PATCH-UPPER-" + str(i),
        alpha=0.0,
        zorder=0,
    )

    # calculate what's inside
    inside_count = 0
    count = 0
    outside_count = 0

    # locate where the observation is outside the prediction interval
    missed_x = []
    missed_y = []
    for j in range(lower_bound, upper_bound):
        if y_training.values[j] < 50.0:
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
        x_forecast_temp[missed_x],
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
        0.75,
        0.7,
        "PI contains "
        + str(round(inside_proportion[i] * 100.0, 1))
        + "%\nof observations",
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
ax_LF.set_title("Loss function", loc="left", color="k", weight="extra bold")
ax_LF.spines["top"].set_visible(False)
ax_LF.spines["right"].set_visible(False)

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
    linestyle="dotted",
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
ax_forecast.set_ylim(0, 100.0)
ax_forecast.set_xlim(np.datetime64(date_range[0]), np.datetime64(date_range[-1]))
start_year = 1971 + np.datetime64(date_range[0], "Y").astype(int)
end_year = 1971 + np.datetime64(date_range[-1], "Y").astype(int)
x_ticks = [np.datetime64(str(i - 1) + label_year) for i in range(start_year, end_year)]
x_ticks_labels = [i + year_label_offset for i in range(start_year, end_year)]
ax_forecast.set_xticks(x_ticks, x_ticks_labels)
ax_forecast.set_yticks(
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
ax_forecast.set_xlabel("Date", weight="semibold")
ax_forecast.set_title(
    "Streamflow percentile",
    loc="left",
    color="k",
    weight="extra bold",
)

set_axis_up(ax_forecast)

# save plots
save_desktop_mobile_tablet(
    dir_1="Task1/out/",
    dir_2="src/assets/svgs/",
    base_name="pi_example",
    fig=fig,
    mobile_dimensions=[
        target_plotwidth_in_mobile,
        target_plotwidth_in_mobile / aspect_double_plot_mobile,
    ],
    tablet_dimensions=[
        target_plotwidth_in_tablet,
        target_plotwidth_in_tablet / aspect_double_plot_tablet,
    ],
    mod_ax_list=[ax_LF, ax_forecast],
    mobile_pos_list=[[0.14, 0.6, 0.8, 0.333], [0.14, 0.1, 0.8, 0.333]],
    tablet_pos_list=[[0.125, 0.575, 0.825, 0.375], [0.125, 0.075, 0.825, 0.375]],
)

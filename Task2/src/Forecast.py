import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime
from scipy import interpolate
import pyarrow.feather as feather
from Task_config.functions import (
    forecast_format,
    forecast_annotations,
    set_axis_up,
    save_desktop_mobile_tablet,
)
from Task_config.setup_matplotlib import (
    target_plotwidth_in_desktop,
    target_plotwidth_in_mobile,
    target_plotwidth_in_tablet,
)

# load in parameters
aspect_double_plot_desktop = snakemake.params["aspect_double_plot_desktop"]
aspect_double_plot_tablet = snakemake.params["aspect_double_plot_tablet"]
aspect_double_plot_mobile = snakemake.params["aspect_double_plot_mobile"]
target_fontsize_px = snakemake.params["target_fontsize_px"]
ratio_7 = snakemake.params["ratio_7"]
median_color_hex = snakemake.params["median_color_hex"]
observation_color_hex = snakemake.params["observation_color_hex"]
site_id = snakemake.params["site_id"]
basename_gid_forecast = snakemake.params["basename_gid_forecast"]
date_range = snakemake.params["date_range"]
label_year = snakemake.params["label_year"]
year_label_offset = snakemake.params["year_label_offset"]


# load data
forecast_data_all = feather.read_feather(snakemake.input[0])
forecast_data_site = forecast_data_all[forecast_data_all["site_id"] == site_id]

# forecast files
forecast_data_list = [
    forecast_data_site[forecast_data_site["nday_forecast"] == 7.0],
    forecast_data_site[forecast_data_site["nday_forecast"] == 14.0],
    forecast_data_site[forecast_data_site["nday_forecast"] == 21.0],
    forecast_data_site[forecast_data_site["nday_forecast"] == 28.0],
    forecast_data_site[forecast_data_site["nday_forecast"] == 35.0],
    forecast_data_site[forecast_data_site["nday_forecast"] == 42.0],
    forecast_data_site[forecast_data_site["nday_forecast"] == 49.0],
    forecast_data_site[forecast_data_site["nday_forecast"] == 56.0],
    forecast_data_site[forecast_data_site["nday_forecast"] == 63.0],
    forecast_data_site[forecast_data_site["nday_forecast"] == 70.0],
    forecast_data_site[forecast_data_site["nday_forecast"] == 77.0],
    forecast_data_site[forecast_data_site["nday_forecast"] == 84.0],
    forecast_data_site[forecast_data_site["nday_forecast"] == 91.0],
]

# plot specific set up
offset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
dt = 7
dense_dt = 1

### Data Arrays

x_forecast_raw = forecast_data_list[0]["datetime"].values.astype("datetime64[D]")
y_training_raw = forecast_data_list[0]["observation"]
y_forecast_lower_raw = forecast_format(forecast_data_list[0]["lower"])
y_forecast_median_raw = forecast_format(forecast_data_list[0]["median"])
y_forecast_upper_raw = forecast_format(forecast_data_list[0]["upper"])

# set a more densly packed dataset (spaced by 1 day instead of 7 days) - this is for the 0-day forecast
x_forecast = np.arange(x_forecast_raw[0], x_forecast_raw[-1], dense_dt)
dx_forecast_raw = (
    x_forecast_raw - x_forecast_raw[0]
)  # difference between current day and first day
dx_forecast = x_forecast - x_forecast[0]  # difference between current day and first day
y_training = interpolate.interp1d(dx_forecast_raw.astype(float), y_training_raw)(
    dx_forecast.astype(float)
)
y_forecast_lower = interpolate.interp1d(
    dx_forecast_raw.astype(float), y_forecast_lower_raw
)(dx_forecast.astype(float))
y_forecast_median = interpolate.interp1d(
    dx_forecast_raw.astype(float), y_forecast_median_raw
)(dx_forecast.astype(float))
y_forecast_upper = interpolate.interp1d(
    dx_forecast_raw.astype(float), y_forecast_upper_raw
)(dx_forecast.astype(float))

# get temporal bounds
lower_bound = np.argmin(np.abs(x_forecast - np.datetime64(date_range[0])))
upper_bound = np.argmin(np.abs(x_forecast - np.datetime64(date_range[1]))) + 1

# set interpolators for the 7,14,28,56,91 - day forcasts
f_cloud_median_list = []
datetime_anchorpoint = forecast_data_list[0]["datetime"].values.astype("datetime64[D]")[
    0
]
for i, forecast_datum in enumerate(forecast_data_list):
    x_forecast_raw_temp = forecast_data_list[i]["datetime"].values.astype(
        "datetime64[D]"
    )

    dx_forecast_raw_temp = (
        x_forecast_raw_temp - datetime_anchorpoint
    )  # this should be right. it should be referenced to the first date, not the start of the array!!!!
    f_cloud_median_list += [
        interpolate.interp1d(
            dx_forecast_raw_temp.astype(float),
            forecast_format(forecast_datum["median"]),
        )
    ]
# make figure
fig = plt.figure(
    1,
    figsize=(
        target_plotwidth_in_desktop,
        target_plotwidth_in_desktop / (aspect_double_plot_desktop * 2.0 / 3.0),
    ),
    gid="figure-" + basename_gid_forecast,
)
# add axes
ax_forecast = fig.add_axes(
    [
        (1.0 - 0.825) / 2.0,
        0.075 * 2.0,
        0.825,
        0.375 * 2.0,
    ],
    gid="axis-" + basename_gid_forecast,
)

# print default value for the vue site
print(
    "the default value to use is "
    + str(np.argmin(np.abs(x_forecast - np.datetime64(date_range[0]))))
)

# generate line
for j in range(lower_bound, upper_bound, int(dt / dense_dt)):
    x_cloud = x_forecast[j] + np.array(offset) * 7
    y_cloud_lower = []
    y_cloud_median = []
    y_cloud_upper = []

    for i in range(0, len(f_cloud_median_list)):
        lead_time = dx_forecast.astype(float)[j + int(offset[i] * dt / dense_dt)]
        y_cloud_median += [f_cloud_median_list[i](lead_time)]

    # observation
    ax_forecast.plot(
        x_forecast[: 1 + j],
        y_training[: 1 + j],
        color=observation_color_hex,
        alpha=0.0,
        gid="observation_" + str(j),
    )

    # hover_line
    target_linewidth = (
        0.825
        * target_plotwidth_in_desktop
        * 72
        / ((upper_bound - lower_bound) / int(dt / dense_dt))
    )
    ax_forecast.plot(
        [x_forecast[j], x_forecast[j]],
        [0, 100],
        color="k",
        alpha=0.0,
        gid="forecast_hover_" + str(j),
        linewidth=target_linewidth,
        zorder=101,
    )

    # # add forecast lines
    ax_forecast.plot(
        x_cloud,
        y_cloud_median,
        color=median_color_hex,
        linestyle="-",
        alpha=0.0,
        gid="forecast_middl_" + str(j),
        solid_capstyle="round",
    )

# add desktop annotations

# limits on x axis with 1 week buffer
x_limits = [np.datetime64(date_range[0]) + 7, np.datetime64(date_range[-1]) - 7]
x_length = x_limits[-1] - x_limits[0]

# annotation for forecast arrow
forecast_annotations(
    ax_forecast,
    [
        "Drag mouse over the plot\nrightwards to see streamflow\ndrought forecasts",
        "Tap on the plot to see\nstreamflow drought forecasts",
        "Tap on the plot to see\nstreamflow drought forecasts",
    ],
    [
        (x_limits[0] + x_length * 0.23, 90),
        (x_limits[0] + x_length * 0.32, 90),
        (x_limits[0] + x_length * 0.57, 90),
    ],
    [
        (x_limits[0], 90),
        (x_limits[0], 90),
        (x_limits[0], 90),
    ],
    target_fontsize_px,
    ratio_7,
    "annotation-1-forecast",
)

# annotation for observation arrow
forecast_annotations(
    ax_forecast,
    [
        "Drag mouse over the\nplot rightwards to see\nstreamflow observations",
        "Tap on the plot to see\nstreamflow observations",
        "Tap on the plot to see\nstreamflow observations",
    ],
    [
        (x_limits[0] + x_length * 0.23, 70),
        (x_limits[0] + x_length * 0.28, 90),
        (x_limits[0] + x_length * 0.60, 90),
    ],
    [
        (x_limits[0], 70),
        (x_limits[0], 90),
        (x_limits[0], 90),
    ],
    target_fontsize_px,
    ratio_7,
    "annotation-1-observation",
)

# annotation for model note arrow
forecast_annotations(
    ax_forecast,
    [
        "Model training prioritizes\naccurate predictions below\nthe 30ᵗʰ percentile",
        "Model training prioritizes\naccurate predictions below\nthe 30ᵗʰ percentile",
        "Model training prioritizes\naccurate predictions below\nthe 30ᵗʰ percentile",
    ],
    [
        (x_limits[0] + x_length * 0.55, 30),
        (x_limits[0] + x_length * 0.55, 30),
        (x_limits[0] + x_length * 0.55, 30),
    ],
    [
        (x_limits[0] + x_length * 0.55, 50),
        (x_limits[0] + x_length * 0.55, 50),
        (x_limits[0] + x_length * 0.55, 55),
    ],
    target_fontsize_px,
    ratio_7,
    "annotation-2-forecast",
    ha="center",
)

# forecast axis parameters
ax_forecast.plot(
    x_forecast,
    y_training,
    color=observation_color_hex,
    linestyle="dotted",
    alpha=0.0,
    gid="observation-full-forecast",
)

# de emphasize above 30
drought_labels = [
    "Normal conditions",
    "Abnormally dry",
    "Moderate streamflow drought",
    "Severe streamflow drought",
    "Extreme streamflow drought",
]
gid_prefixes = ["obsv-nm-", "obsv-ad-", "obsv-md-", "obsv-sd-", "obsv-ed-"]
drought_label_lines = [40, 30, 20, 10, 5, 0]
fontsizes = [target_fontsize_px, 0.8 * target_fontsize_px]
for j, platform in enumerate(["", "-tablet"]):
    for i, drought_label in enumerate(drought_labels):
        ax_forecast.text(
            x_limits[-1],
            0.5 * (drought_label_lines[i] + drought_label_lines[i + 1]),
            drought_label,
            ha="right",
            va="center",
            fontsize=fontsizes[j],
            gid=gid_prefixes[i] + "label" + platform,
            alpha=0.0,
        )
        ax_forecast.plot(
            [np.datetime64(date_range[0]), np.datetime64(date_range[-1])],
            [drought_label_lines[i], drought_label_lines[i]],
            color="k",
            linestyle="--",
            gid=gid_prefixes[i] + "line" + platform,
            alpha=0.0,
        )

ax_forecast.fill_between(
    [np.datetime64(date_range[0]), np.datetime64(date_range[-1])],
    [30, 30],
    [100, 100],
    edgecolor="none",
    facecolor="w",
    alpha=0.00001,
    zorder=99,
    gid="forecast-washout",
)

# Make a legend
legend_elements = 6

for legend_element in range(0, legend_elements):
    if legend_element == (legend_elements / 2) - 1:
        labelcolor = (ratio_7,)
        # create dummy lines for observation to make legend
        (obs_line,) = ax_forecast.plot(
            [0, 1],
            [-10, -10],
            color=observation_color_hex,
            linestyle="dotted",
            alpha=1.0,
        )
    else:
        labelcolor = [0, 0, 0, 0]
        # create dummy lines for observation to make legend
        (obs_line,) = ax_forecast.plot(
            [0, 1],
            [-10, -10],
            color="none",
            linestyle="dotted",
            alpha=1.0,
        )

    # create dummy lines for forecast to make legend
    (for_line,) = ax_forecast.plot(
        [0, 1],
        [-10, -10],
        color=median_color_hex,
        linestyle="-",
        linewidth=2.0 - legend_element * 0.2,
        alpha=1.0 - legend_element * 0.2,
        solid_capstyle="round",
    )

    legend = ax_forecast.legend(
        handles=[obs_line, for_line],
        bbox_to_anchor=(1.0, 1.0 - legend_element * 0.01),
        labels=["Observation", "Forecasts"],
        loc="upper right",
        edgecolor="none",
        facecolor="none",
        ncols=2,
        labelcolor=labelcolor,
    )
    legend.set_zorder(100)
    legend.set(gid="forecast-legend-" + str(legend_element))
    ax_forecast.add_artist(legend)

# forecast axis parameters
ax_forecast.grid(visible=True, axis="y")
ax_forecast.set_ylim(0, 100.0)
ax_forecast.set_xlim(
    np.datetime64(date_range[0]),
    np.datetime64(date_range[-1]),
)
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
ax_forecast.set_ylabel(
    "Streamflow percentile",
    weight="semibold",
    gid="observation-forecast-ylabel",
)
ax_forecast.set_title(
    "Streamflow percentile",
    loc="left",
    weight="extra bold",
    color="k",
    gid="observation-forecast-title",
)

set_axis_up(ax_forecast)

# save plots
save_desktop_mobile_tablet(
    dir_1="Task2/out/",
    dir_2="src/assets/svgs/",
    base_name="fc_example",
    fig=fig,
    mobile_dimensions=[
        target_plotwidth_in_mobile,
        target_plotwidth_in_mobile / aspect_double_plot_mobile * 0.5,
    ],
    tablet_dimensions=[
        target_plotwidth_in_tablet,
        target_plotwidth_in_tablet / aspect_double_plot_tablet * 0.5,
    ],
    mod_ax_list=[ax_forecast],
    mobile_pos_list=[[0.14, 0.175, 0.8, 0.333 * 2.0]],
    tablet_pos_list=[[0.125, 0.125, 0.825, 0.375 * 2.0]],
)

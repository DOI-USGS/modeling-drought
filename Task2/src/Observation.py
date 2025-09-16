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
forecast_data_list = [forecast_data_site[forecast_data_site["nday_forecast"] == 7.0]]

# plot specific set up
offset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
dt = 7
dense_dt = 1

# Shorten x-axis in mobile site
x_shorten_mobile = 0.575
x_label_section_mobile = x_shorten_mobile + 0.075

### Data Arrays

x_forecast_raw = forecast_data_list[0]["datetime"].values.astype("datetime64[D]")
y_training_raw = forecast_data_list[0]["observation"]

# set a more densly packed dataset (spaced by 1 day instead of 7 days) - this is for the 0-day forecast
x_forecast = np.arange(x_forecast_raw[0], x_forecast_raw[-1], dense_dt)
dx_forecast_raw = (
    x_forecast_raw - x_forecast_raw[0]
)  # difference between current day and first day
dx_forecast = x_forecast - x_forecast[0]  # difference between current day and first day
y_training = interpolate.interp1d(dx_forecast_raw.astype(float), y_training_raw)(
    dx_forecast.astype(float)
)

# get temporal bounds
lower_bound = np.argmin(np.abs(x_forecast - np.datetime64(date_range[0])))
upper_bound = np.argmin(np.abs(x_forecast - np.datetime64(date_range[1]))) + 1

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
        0.825 * x_shorten_mobile,
        0.375 * 2.0,
    ],
    gid="axis-" + basename_gid_forecast,
)

# generate line
for j in range(lower_bound, upper_bound, int(dt / dense_dt)):

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

# annotation for observation arrow
x_limits = [np.datetime64(date_range[0]), np.datetime64(date_range[-1])]

ax_forecast.annotate(
    "Tap on the plot to see\nstreamflow observations",
    color=ratio_7,
    va="center",
    ha="left",
    fontsize=0.8 * target_fontsize_px,
    xy=(x_limits[0] + 7 + 0.5 * (x_limits[-1] - x_limits[0]), 90),
    xytext=(x_limits[0] + 7, 90),
    arrowprops=dict(
        facecolor=ratio_7,
        edgecolor=ratio_7,
        alpha=1,
        arrowstyle="fancy",
        gid="annotation-1-observation-arrow-mobile",
    ),
    gid="annotation-1-observation-mobile",
    alpha=1.0,
    zorder=100,
)

# de emphasize above 30
drought_labels = [
    "Abnormally dry",
    "Moderate\nstreamflow drought",
    "Severe\nstreamflow drought",
    "Extreme\nstreamflow drought",
]
gid_prefixes = ["obsv-ad-", "obsv-md-", "obsv-sd-", "obsv-ed-"]
x_length = x_limits[-1] - x_limits[0]
y_drought_lines = [30, 20, 10, 5]
y_drought_label_lines = [80, 60, 40, 20, 0]
y_drought_labels = [70, 50, 30, 10]
platform = "-mobile"

x_drought_label_line = [
    x_limits[0] + x_length * x_shorten_mobile,
    x_limits[0] + x_length * x_label_section_mobile,
    x_limits[-1],
]

ax_forecast.text(
    x_drought_label_line[1] + 7,
    90,
    "Normal conditions",
    ha="left",
    va="center",
    fontsize=0.8 * target_fontsize_px,
    gid="obsv-nm-label" + platform,
)

for i, drought_label in enumerate(drought_labels):
    ax_forecast.text(
        x_drought_label_line[1] + 14,
        y_drought_labels[i],
        drought_labels[i],
        ha="left",
        va="center",
        fontsize=0.8 * target_fontsize_px,
        gid=gid_prefixes[i] + "label" + platform,
        alpha=0.0,
    )
    ax_forecast.plot(
        x_limits,
        [y_drought_lines[i], y_drought_lines[i]],
        color="k",
        linestyle="--",
        gid=gid_prefixes[i] + "line" + platform,
        alpha=0.0,
    )
    ax_forecast.plot(
        x_drought_label_line,
        [y_drought_lines[i], y_drought_label_lines[i], y_drought_label_lines[i]],
        color="k",
        linestyle="--",
        clip_on=False,
        alpha=0.0,
        gid=gid_prefixes[i] + "slopeline" + platform,
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

ax_forecast.grid(visible=True, axis="y")
ax_forecast.set_ylim(0, 100.0)
ax_forecast.set_xlim(
    x_limits[0],
    x_limits[0] + x_length * (x_shorten_mobile),
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
    base_name="ob_example",
    fig=fig,
    mobile_dimensions=[
        target_plotwidth_in_mobile,
        target_plotwidth_in_mobile / aspect_double_plot_mobile * 0.5,
    ],
    tablet_dimensions=[],
    mod_ax_list=[ax_forecast],
    mobile_pos_list=[[0.15, 0.175, 0.8 * x_shorten_mobile, 0.333 * 2.0]],
    tablet_pos_list=[[]],
    save_desktop=False,
    save_tablet=False,
    save_mobile=True,
)

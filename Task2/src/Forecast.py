import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime
from scipy import interpolate
import pyarrow.feather as feather
from Task_config.defaults import *
from Task_config.functions import *
from Task_config.parameters import *

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

    # exit()
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
        zorder=100,
    )

    # # add forecast lines
    ax_forecast.plot(
        x_cloud,
        y_cloud_median,
        color="k",
        linestyle="-",
        alpha=0.0,
        gid="forecast_middl_" + str(j),
        solid_capstyle="round",
    )

# add desktop annotation
ax_forecast.annotate(
    "Drag mouse over the\nplot rightwards to see\ndrought forecasts",
    color=ratio_5,
    va="center",
    xy=(np.datetime64(date_range[0]) + 147, 50),
    xytext=(np.datetime64(date_range[0]) + 7, 50),
    arrowprops=dict(
        facecolor=ratio_5,
        edgecolor=ratio_5,
        alpha=0.00001,
        arrowstyle="fancy",
        gid="annotation_forecast_arrow",
    ),
    gid="annotation_forecast",
    alpha=0.0,
    zorder=100,
)

# add mobile annotation
ax_forecast.annotate(
    "Tap on the plot to\nsee drought forecasts",
    color=ratio_5,
    va="center",
    xy=(np.datetime64(date_range[0]) + 400, 50),
    xytext=(np.datetime64(date_range[0]) + 7, 50),
    arrowprops=dict(
        facecolor=ratio_5,
        edgecolor=ratio_5,
        alpha=0.0001,
        arrowstyle="fancy",
        gid="annotation_forecast_arrow_mobile",
    ),
    gid="annotation_forecast_mobile",
    alpha=0.0,
    zorder=100,
)

# add tablet annotation
ax_forecast.annotate(
    "Tap on the plot to\nsee drought forecasts",
    color=ratio_5,
    va="center",
    xy=(np.datetime64(date_range[0]) + 230, 50),
    xytext=(np.datetime64(date_range[0]) + 7, 50),
    arrowprops=dict(
        facecolor=ratio_5,
        edgecolor=ratio_5,
        alpha=0.00001,
        arrowstyle="fancy",
        gid="annotation_forecast_arrow_tablet",
    ),
    gid="annotation_forecast_tablet",
    alpha=0.0,
    zorder=100,
)

# forecast axis parameters
ax_forecast.plot(
    x_forecast,
    y_training,
    color="tab:red",
    linestyle=obs_linestyle,
    alpha=0.0,
    gid="observation-full-forecast",
)

# de emphasize above 30
ax_forecast.plot(
    [np.datetime64(date_range[0]), np.datetime64(date_range[-1])],
    [30, 30],
    color="k",
    linestyle="--",
)
ax_forecast.fill_between(
    [np.datetime64(date_range[0]), np.datetime64(date_range[-1])],
    [30, 30],
    [100, 100],
    edgecolor="none",
    facecolor="w",
    alpha=0.75,
    zorder=99,
)

ax_forecast.grid(visible=True, axis="y")
ax_forecast.set_ylim(0, 100.0)
ax_forecast.set_xlim(np.datetime64(date_range[0]), np.datetime64(date_range[-1]))
start_year = 1971 + np.datetime64(date_range[0], "Y").astype(int)
end_year = 1971 + np.datetime64(date_range[-1], "Y").astype(int)
x_ticks = [np.datetime64(str(i) + "-01-01") for i in range(start_year, end_year)]
x_ticks_labels = [i for i in range(start_year, end_year)]
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
    "Streamflow percentile", loc="left", weight="extra bold", color="k"
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

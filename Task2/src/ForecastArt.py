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
y_forecast_median = interpolate.interp1d(
    dx_forecast_raw.astype(float), y_forecast_median_raw
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
)
# add axes
ax_forecast = fig.add_axes(
    [0, 0, 1, 1],
)

# generate line
number_of_lines = 11
start_forecast = lower_bound + 31 * 7
end_forecast = start_forecast + number_of_lines * 2 * 7
k = 0.0
for j in range(start_forecast, end_forecast, int(dt / dense_dt * 2)):
    x_cloud = x_forecast[j] + np.array(offset) * 7
    y_cloud_lower = []
    y_cloud_median = []
    y_cloud_upper = []

    for i in range(0, len(f_cloud_median_list)):
        lead_time = dx_forecast.astype(float)[j + int(offset[i] * dt / dense_dt)]
        y_cloud_median += [f_cloud_median_list[i](lead_time)]

    # # add forecast lines
    ax_forecast.plot(
        x_cloud,
        y_cloud_median,
        color=median_color_hex,
        linestyle="-",
        alpha=k / number_of_lines * 0.9 + 0.1,
        solid_capstyle="round",
        linewidth=4.0 + 2.0 * k / number_of_lines,
        solid_joinstyle="round",
        zorder=2,
    )
    k += 1

# forecast axis parameters
ax_forecast.plot(
    x_forecast,
    y_training,
    color=observation_color_hex,
    # linestyle="dotted",
    alpha=1.0,
    linewidth=3.0,
    solid_capstyle="round",
    solid_joinstyle="round",
    zorder=1,
)

# forecast axis parameters
ax_forecast.set_ylim(-5, 75)
ax_forecast.set_xlim(
    np.datetime64(date_range[0])
    + 0.125 * (np.datetime64(date_range[1]) - np.datetime64(date_range[0])),
    np.datetime64(date_range[-1])
    - 0.125 * (np.datetime64(date_range[1]) - np.datetime64(date_range[0])),
)
ax_forecast.set_axis_off()

# save plots
save_desktop_mobile_tablet(
    dir_1="Task2/out/",
    dir_2="src/assets/svgs/",
    base_name="fc_art",
    fig=fig,
    mobile_dimensions=[],
    tablet_dimensions=[],
    mod_ax_list=[ax_forecast],
    mobile_pos_list=[[]],
    tablet_pos_list=[[]],
    save_desktop=True,
    save_tablet=False,
    save_mobile=False,
)

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime
from scipy import interpolate
import pyarrow.feather as feather
import re
import os
from Task_config.defaults import *
from Task_config.functions import *
from Task_config.parameters import *

### Data Arrays

# load the raw data - 0 day forecast
forecast_data = [
    feather.read_feather("Task_Data/" + forecast_file)
    for forecast_file in forecast_files
]
x = np.linspace(0.0, 13.0, 14)
index_plot = 158
y_issue_date = list(forecast_data[0]["observed"])[index_plot - 1]
y = [y_issue_date]
y += list(forecast_data[0]["median"])[index_plot : index_plot + 13]

# make figure
fig = plt.figure(
    1,
    figsize=(
        target_plotwidth_in_mobile,
        target_plotwidth_in_mobile / aspect_single_plot,
    ),
    gid="figure-forecast-diagram",
)

# add axes
ax_forecast = fig.add_axes(
    [0.05, 0.15, 0.9, 0.75],
    gid="axis-forecast-diagram" + basename_gid_forecast,
)

# add line
ax_forecast.plot(
    x,
    y,
    color=median_color_hex,
    alpha=1.0,
    linewidth=2.0,
    zorder=1,
)
# add white dots
ax_forecast.scatter(
    0.0,
    y_issue_date,
    s=100,
    edgecolor=median_color_hex,
    alpha=1.0,
    facecolor="w",
    zorder=2,
)
# add blue dots
ax_forecast.scatter(
    x[1:],
    y[1:],
    s=100,
    edgecolor=median_color_hex,
    alpha=1.0,
    facecolor=median_color_hex,
    zorder=2,
)
# add issue date text
ax_forecast.text(
    0.0,
    y_issue_date + 2.0,
    "Issue\ndate",
    color=median_color_hex,
    weight="semibold",
    ha="center",
    va="bottom",
)

# set up axes
ax_forecast.tick_params(direction="out")
ax_forecast.set_xlim(-1.0, 14.0)
ax_forecast.set_xticks(
    [1.0, 13.0],
    [
        "1",
        "13",
    ],
    weight="regular",
)
ax_forecast.set_xlabel("Forecast horizon in weeks", weight="semibold")
ax_forecast.set_title(
    "Streamflow percentile", loc="left", weight="extra bold", color="k"
)
ax_forecast.spines["top"].set_visible(False)
ax_forecast.spines["right"].set_visible(False)
ax_forecast.spines["left"].set_visible(False)
ax_forecast.yaxis.set_visible(False)
ax_forecast.set_axisbelow(True)
ax_forecast.set_ylim(20, 80)

# river label
plt.figtext(1, 0, river_label, ha="right", va="bottom", alpha=0.5)

# make svg
fig.savefig("Task2/out/fc_diagram.png", dpi=150)
fig.savefig("Task2/out/fc_diagram.svg", metadata=None)

# remove metadata
remove_metadata_and_fix("Task2/out/fc_diagram.svg", "src/assets/svgs/fc_diagram.svg")

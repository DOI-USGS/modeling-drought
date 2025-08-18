import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pyarrow.feather as feather
from Task_config.defaults import *
from Task_config.functions import *
from Task_config.parameters import *

# plotting variables
x = np.linspace(0.0, 13.0, 14)
y_issue_date = list(forecast_data_diagram["observed"])[index_plot - 1]
y = [y_issue_date]
y += list(forecast_data_diagram["median"])[index_plot : index_plot + 13]

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
ax_forecast.spines["left"].set_visible(False)
ax_forecast.yaxis.set_visible(False)
ax_forecast.set_ylim(20, 80)

set_axis_up(ax_forecast)

# make svg
fig.savefig("Task2/out/fc_diagram.svg", metadata=None)

# remove metadata
remove_metadata_and_fix("Task2/out/fc_diagram.svg", "src/assets/svgs/fc_diagram.svg")

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

### Data Arrays
# load drought data
tf_d = pd.read_csv(
    "Task_Data/UQ_summaries_for_JeffreyHayley_4PanelClassificationTypesForDroughtOnly_DataCounts_interpolated.csv"
)

horizon_weeks = tf_d["horizon"]
total = tf_d["true_pos"] + tf_d["false_pos"] + tf_d["false_neg"] + tf_d["true_neg"]

D_D_list = tf_d["true_pos"] / total * 100.0
D_ND_list = tf_d["false_pos"] / total * 100.0 + D_D_list

ND_D_list = tf_d["false_neg"] / total * 100.0 + D_ND_list
ND_ND_list = tf_d["true_neg"] / total * 100.0 + ND_D_list


# make figure
fig_true_false = plt.figure(
    1,
    figsize=(
        target_single_plotwidth,
        target_single_plotwidth / aspect_single_plot,
    ),
    gid="figure-" + basename_gid_true_false_summary,
)
# add axes for the forecast
ax_true_false = fig_true_false.add_axes(
    [0.1, 0.15, 0.85, 0.75], gid="axis-" + basename_gid_true_false_summary
)


# labeling
text_bump = 0.5
label_pad = 0.1
for i in range(0, len(tf_d)):

    ax_true_false.fill_between(
        [i + label_pad, i + 1 - label_pad],
        [D_D_list[i], D_D_list[i]],
        [0.0, 0.0],
        facecolor=lower_color_limit_hex,
        # edgecolor=ratio_7,
    )
    ax_true_false.fill_between(
        [i + label_pad, i + 1 - label_pad],
        [D_ND_list[i], D_ND_list[i]],
        [D_D_list[i], D_D_list[i]],
        facecolor=lower_color_limit_hex_half_alpha,
        # hatch="/",
        # edgecolor=ratio_5,
        # linewidth=0.0,
    )
    ax_true_false.fill_between(
        [i + label_pad, i + 1 - label_pad],
        [ND_D_list[i], ND_D_list[i]],
        [D_ND_list[i], D_ND_list[i]],
        facecolor=upper_color_limit_hex_half_alpha,
        # hatch="\\",
        # edgecolor=ratio_5,
        # linewidth=0.0,
    )
    ax_true_false.fill_between(
        [i + label_pad, i + 1 - label_pad],
        [ND_ND_list[i], ND_ND_list[i]],
        [ND_D_list[i], ND_D_list[i]],
        facecolor=upper_color_limit_hex,
        # edgecolor=ratio_7,
    )

    ax_true_false.plot(
        [i + label_pad, i + 1 - label_pad],
        [D_ND_list[i], D_ND_list[i]],
        color=ratio_7,
        linewidth=2.0,
    )


ax_true_false.set_ylim(0, 100)
# ax_true_false.set_xlim(0, 5)
ax_true_false.set_yticks(
    [0.0, 20.0, 40.0, 60.0, 80.0, 100], ["0%", "20%", "40%", "60%", "80%", "100%"]
)
ax_true_false.set_xticks(np.linspace(1, 13, 13) - 0.5, [str(i) for i in range(1, 14)])
ax_true_false.set_title(
    "Model outcomes",
    loc="left",
    weight="extra bold",
    color="k",
)
ax_true_false.spines["top"].set_visible(False)
ax_true_false.spines["right"].set_visible(False)
ax_true_false.set_xlabel("Forecast horizon in weeks", weight="semibold")
ax_true_false.grid(visible=True, axis="y")
ax_true_false.set_axisbelow(True)
ax_true_false.tick_params(direction="out")

# make svg
fig_true_false.savefig("Task2/out/fc_tf_sum_desktop.png", dpi=400, metadata=None)
fig_true_false.savefig("Task2/out/fc_tf_sum_desktop.svg", dpi=150, metadata=None)

# remove metadata
remove_metadata_and_fix(
    "Task2/out/fc_tf_sum_desktop.svg",
    "src/assets/svgs/fc_tf_sum_desktop.svg",
)

# to make the mobile version, we first adjust the figure size to a more horizontal aspect
fig_true_false.set_size_inches(
    target_plotwidth_in_mobile,
    target_plotwidth_in_mobile / aspect_single_plot,
)

# make svg
fig_true_false.savefig("Task2/out/fc_tf_sum_mobile.svg", metadata=None)

# remove metadata
remove_metadata_and_fix(
    "Task2/out/fc_tf_sum_mobile.svg",
    "src/assets/svgs/fc_tf_sum_mobile.svg",
)

# to make the tablet version, we first adjust the figure size to a more horizontal aspect
fig_true_false.set_size_inches(
    target_plotwidth_in_tablet,
    target_plotwidth_in_tablet / aspect_single_plot,
)

# make svg
fig_true_false.savefig("Task2/out/fc_tf_sum_tablet.svg", metadata=None)

# remove metadata
remove_metadata_and_fix(
    "Task2/out/fc_tf_sum_tablet.svg",
    "src/assets/svgs/fc_tf_sum_tablet.svg",
)

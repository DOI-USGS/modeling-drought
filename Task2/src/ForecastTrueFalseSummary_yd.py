### Import Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Task_config.defaults import *
from Task_config.functions import *
from Task_config.parameters import *

# compute rights and wrongs
horizon_weeks = tf_d["horizon"]
total = tf_d["true_pos"] + tf_d["false_pos"]

D_D_list = tf_d["true_pos"] / total * 100.0
D_ND_list = tf_d["false_pos"] / total * 100.0 + D_D_list

# make figure
fig_true_false = plt.figure(
    1,
    figsize=(
        target_single_plotwidth,
        target_single_plotwidth / aspect_single_plot,
    ),
    gid="figure-" + basename_gid_true_false_summary + "-yd",
)
# add axes for the forecast
ax_true_false = fig_true_false.add_axes(
    [0.1, 0.15, 0.85, 0.75], gid="axis-" + basename_gid_true_false_summary + "-yd"
)

# plot for each day
for i in range(0, len(tf_d)):
    # true positive
    ax_true_false.fill_between(
        [i + label_pad, i + 1 - label_pad],
        [D_D_list[i], D_D_list[i]],
        [0.0, 0.0],
        facecolor=lower_color_limit_hex,
    )
    # false positive
    ax_true_false.fill_between(
        [i + label_pad, i + 1 - label_pad],
        [D_ND_list[i], D_ND_list[i]],
        [D_D_list[i], D_D_list[i]],
        facecolor=lower_color_limit_hex_half_alpha,
    )

# set axes parameters
ax_true_false.set_ylim(0, 100)
ax_true_false.set_yticks(
    [0.0, 20.0, 40.0, 60.0, 80.0, 100], ["0%", "20%", "40%", "60%", "80%", "100%"]
)
ax_true_false.set_xticks(np.linspace(1, 13, 13) - 0.5, [str(i) for i in range(1, 14)])
ax_true_false.set_title(
    "When drought is predicted",
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
fig_true_false.savefig("Task2/out/fc_tf_sum_yd_desktop.png", dpi=400, metadata=None)
fig_true_false.savefig("Task2/out/fc_tf_sum_yd_desktop.svg", dpi=150, metadata=None)

# remove metadata
remove_metadata_and_fix(
    "Task2/out/fc_tf_sum_yd_desktop.svg",
    "src/assets/svgs/fc_tf_sum_yd_desktop.svg",
)

# to make the mobile version, we first adjust the figure size to a more horizontal aspect
fig_true_false.set_size_inches(
    target_plotwidth_in_mobile,
    target_plotwidth_in_mobile / aspect_single_plot,
)

# make svg
fig_true_false.savefig("Task2/out/fc_tf_sum_yd_mobile.svg", metadata=None)

# remove metadata
remove_metadata_and_fix(
    "Task2/out/fc_tf_sum_yd_mobile.svg",
    "src/assets/svgs/fc_tf_sum_yd_mobile.svg",
)


# to make the tablet version, we first adjust the figure size to a more horizontal aspect
fig_true_false.set_size_inches(
    target_plotwidth_in_tablet,
    target_plotwidth_in_tablet / aspect_single_plot,
)

# make svg
fig_true_false.savefig("Task2/out/fc_tf_sum_yd_tablet.svg", metadata=None)

# remove metadata
remove_metadata_and_fix(
    "Task2/out/fc_tf_sum_yd_tablet.svg",
    "src/assets/svgs/fc_tf_sum_yd_tablet.svg",
)

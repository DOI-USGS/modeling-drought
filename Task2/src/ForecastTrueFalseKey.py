### Import Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Task_config.defaults import *
from Task_config.functions import *
from Task_config.parameters import *

### Data Arrays

i = 0
total = (
    tf_d["true_pos"][i]
    + tf_d["false_pos"][i]
    + tf_d["false_neg"][i]
    + tf_d["true_neg"][i]
)
D = (tf_d["true_pos"][i] + tf_d["false_pos"][i]) / total * 100.0
D_D = tf_d["true_pos"][i] / total * 100.0
D_ND = tf_d["false_pos"][i] / total * 100.0
ND = (tf_d["true_neg"][i] + tf_d["false_neg"][i]) / total * 100.0
ND_D = tf_d["false_neg"][i] / total * 100.0
ND_ND = tf_d["true_neg"][i] / total * 100.0

### Plotting

# make figure
fig_true_false = plt.figure(
    5,
    figsize=(
        target_single_plotwidth,
        target_single_plotwidth / aspect_single_plot,
    ),
    gid="figure-" + basename_gid_true_false_key,
)
# add axes for the forecast
ax_true_false = fig_true_false.add_axes(
    [0.0, 0.0, 1.0, 1.0], gid="axis-" + basename_gid_true_false_key
)


# Section 1 - one bar: all results and two swoops: for drought or no drought
# bar
ax_true_false.fill_between(
    [row0 - width * 0.5, row0 + width * 0.5],
    [ND, ND],
    [-D, -D],
    color="#00264c",
    linewidth=0.0,
)
# label
sankey_label(
    ax_true_false, row0, 0.0, (ND - D), "All model\npredictions", "right", -width
)
# swoops
sankey_swoop(
    ax_true_false,
    row0,
    row1,
    width,
    0.0,
    0.5 * pad,
    ND,
    upper_color_limit_hex,
    swoop_alpha,
    gid="tf-swoop-ND",
)
sankey_swoop(
    ax_true_false,
    row0,
    row1,
    width,
    0.0,
    -0.5 * pad,
    -D,
    lower_color_limit_hex,
    swoop_alpha,
    gid="tf-swoop-YD",
)


# Section 2 - two bars: for drought or no drought and four swoops: for true/false positive/negative
# bars
sankey_bar(
    ax_true_false,
    row1,
    0.5 * pad,
    ND,
    width,
    upper_color_limit_hex,
    bar_alpha,
    gid="tf-bar-ND",
)
sankey_bar(
    ax_true_false,
    row1,
    -0.5 * pad,
    D,
    width,
    lower_color_limit_hex,
    bar_alpha,
    gid="tf-bar-YD",
)
# labels
sankey_label(
    ax_true_false,
    row1,
    -0.5 * pad,
    -D,
    "Model predicts\ndrought - " + str(round(D, 1)) + "%",
    "right",
    -width,
    label_alpha,
    gid="tf-label-YD",
)
sankey_label(
    ax_true_false,
    row1,
    0.5 * pad,
    ND,
    "Model predicts\nno drought - " + str(round(ND, 1)) + "%",
    "right",
    -width,
    label_alpha,
    gid="tf-label-ND",
)

# swoops
sankey_swoop(
    ax_true_false,
    row1,
    row2,
    width,
    -0.5 * pad,
    -pad,
    -D_ND,
    lower_color_limit_hex_half_alpha,
    swoop_alpha,
    gid="tf-swoop-YD-ND",
)
sankey_swoop(
    ax_true_false,
    row1,
    row2,
    width,
    -0.5 * pad - D_ND,
    -2.0 * pad - D_ND,
    -D_D,
    lower_color_limit_hex,
    swoop_alpha,
    gid="tf-swoop-YD-YD",
)

sankey_swoop(
    ax_true_false,
    row1,
    row2,
    width,
    0.5 * pad,
    pad,
    ND_D,
    upper_color_limit_hex_half_alpha,
    swoop_alpha,
    gid="tf-swoop-ND-YD",
)

sankey_swoop(
    ax_true_false,
    row1,
    row2,
    width,
    0.5 * pad + ND_D,
    2.0 * pad + ND_D,
    ND_ND,
    upper_color_limit_hex,
    swoop_alpha,
    gid="tf-swoop-ND-ND",
)

# Section 3 - four bars: for true/false positive/negative
# bars
sankey_bar(
    ax_true_false,
    row2,
    -2.0 * pad - D_ND,
    D_D,
    width,
    lower_color_limit_hex,
    bar_alpha,
    gid="tf-bar-YD-YD",
)
sankey_bar(
    ax_true_false,
    row2,
    -1.0 * pad,
    D_ND,
    width,
    lower_color_limit_hex_half_alpha,
    bar_alpha,
    gid="tf-bar-YD-ND",
)
sankey_bar(
    ax_true_false,
    row2,
    1.0 * pad,
    ND_D,
    width,
    upper_color_limit_hex_half_alpha,
    bar_alpha,
    gid="tf-bar-ND-YD",
)
sankey_bar(
    ax_true_false,
    row2,
    2.0 * pad + ND_D,
    ND_ND,
    width,
    upper_color_limit_hex,
    bar_alpha,
    gid="tf-bar-ND-ND",
)
# labels
sankey_label(
    ax_true_false,
    row2,
    -2.0 * pad - D_ND,
    -D_D,
    "Model detected\nthe drought\n(true positive)\n" + str(round(D_D, 1)) + "%",
    "right",
    -width,
    label_alpha,
    gid="tf-label-YD-YD",
)
sankey_label(
    ax_true_false,
    row2,
    -1.0 * pad,
    -D_ND,
    "Model wrongly\npredicted drought\n(false positive)\n" + str(round(D_ND, 1)) + "%",
    "right",
    -width,
    label_alpha,
    gid="tf-label-YD-ND",
)
sankey_label(
    ax_true_false,
    row2,
    1.0 * pad,
    ND_D,
    "Model missed\nthe drought\n(false negative)\n" + str(round(ND_D, 1)) + "%",
    "right",
    -width,
    label_alpha,
    gid="tf-label-ND-YD",
)
sankey_label(
    ax_true_false,
    row2,
    2.0 * pad + ND_D,
    ND_ND,
    "No drought\noccurred\n(true negative)\n" + str(round(ND_ND, 1)) + "%",
    "right",
    -width,
    label_alpha,
    gid="tf-label-ND-ND",
)

# set axis parameters
ax_true_false.set_xlim(-5)
ax_true_false.set_axis_off()

# save plots
save_desktop_mobile_tablet(
    dir_1="Task2/out/",
    dir_2="src/assets/svgs/",
    base_name="fc_tf_key",
    fig=fig_true_false,
    mobile_dimensions=[
        target_plotwidth_in_mobile,
        target_plotwidth_in_mobile / aspect_single_plot,
    ],
    tablet_dimensions=[
        target_plotwidth_in_tablet,
        target_plotwidth_in_tablet / aspect_single_plot,
    ],
)

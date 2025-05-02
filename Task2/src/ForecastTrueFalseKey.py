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
    "Task_Data/UQ_summaries_for_JeffreyHayley_4PanelClassificationTypesForDroughtOnly_DataCounts.csv"
)

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

pad = 5.0
width = 1.0

row0 = 0.0
row1 = 10.0
row2 = 20.0

bar_alpha = 0.25
swoop_alpha = 0.05
label_alpha = 0.0
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


# row 0
ax_true_false.fill_between(
    [row0 - width * 0.5, row0 + width * 0.5],
    [ND, ND],
    [-D, -D],
    color="#00264c",
    linewidth=0.0,
)
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

sankey_label(
    ax_true_false, row0, 0.0, (ND - D), "All model\npredictions", "right", -width
)

# row 1
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

sankey_label(
    ax_true_false,
    row1,
    -0.5 * pad,
    -D,
    "Model predicts drought",
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
    "Model predicts no drought",
    "right",
    -width,
    label_alpha,
    gid="tf-label-ND",
)

# row 2
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

sankey_label(
    ax_true_false,
    row2,
    -2.0 * pad - D_ND,
    -D_D,
    "Model correctly\npredicted drought\n(True Positive)",
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
    "Model wrongly\npredicted drought\n(False Positive)",
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
    "Model missed\nthe drought\n(False Negative)",
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
    "Model correctly\npredicted no drought\n(True Negative)",
    "right",
    -width,
    label_alpha,
    gid="tf-label-ND-ND",
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

ax_true_false.set_xlim(-5)
ax_true_false.set_axis_off()

# make svg
fig_true_false.savefig("Task2/out/fc_tf_key_desktop.png", dpi=400, metadata=None)
fig_true_false.savefig("Task2/out/fc_tf_key_desktop.svg", dpi=150, metadata=None)

# remove metadata
remove_metadata_and_fix(
    "Task2/out/fc_tf_key_desktop.svg",
    "src/assets/svgs/fc_tf_key_desktop.svg",
)

# to make the mobile version, we first adjust the figure size to a more horizontal aspect
fig_true_false.set_size_inches(
    target_plotwidth_in_mobile,
    target_plotwidth_in_mobile / aspect_single_plot,
)

# make svg
fig_true_false.savefig("Task2/out/fc_tf_key_mobile.svg", metadata=None)

# remove metadata
remove_metadata_and_fix(
    "Task2/out/fc_tf_key_mobile.svg",
    "src/assets/svgs/fc_tf_key_mobile.svg",
)

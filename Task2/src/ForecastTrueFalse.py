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

total_list = []
D_list = []
ND_list = []
D_D_list = []
D_ND_list = []
ND_D_list = []
ND_ND_list = []

for i in range(0, len(tf_d)):
    total = (
        tf_d["true_pos"][i]
        + tf_d["false_pos"][i]
        + tf_d["false_neg"][i]
        + tf_d["true_neg"][i]
    )
    total_list += [total]
    D_list += [(tf_d["true_pos"][i] + tf_d["false_pos"][i]) / total * 100.0]
    D_D_list += [tf_d["true_pos"][i] / total * 100.0]
    D_ND_list += [tf_d["false_pos"][i] / total * 100.0]
    ND_list += [(tf_d["true_neg"][i] + tf_d["false_neg"][i]) / total * 100.0]
    ND_D_list += [tf_d["false_neg"][i] / total * 100.0]
    ND_ND_list += [tf_d["true_neg"][i] / total * 100.0]

pad = 5.0
width = 1.0

row0 = 0.0
row1 = 10.0
row2 = 20.0

horizons = ["01wk", "02wk", "04wk", "8wk", "13wk"]

for i in range(0, 5):
    ### Plotting

    # make figure
    fig_true_false = plt.figure(
        i,
        figsize=(
            target_single_plotwidth,
            target_single_plotwidth / aspect_single_plot,
        ),
        gid="figure-" + basename_gid_true_false,
    )
    # add axes for the forecast
    ax_true_false = fig_true_false.add_axes(
        [0.0, 0.0, 1.0, 1.0], gid="axis-" + basename_gid_true_false
    )

    D = D_list[i]
    ND = ND_list[i]

    D_D = D_D_list[i]
    D_ND = D_ND_list[i]
    ND_D = ND_D_list[i]
    ND_ND = ND_ND_list[i]

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
    )

    sankey_label(
        ax_true_false, row0, 0.0, (ND - D), "All Predictions\n100%", "right", -width
    )

    # row 1
    sankey_bar(ax_true_false, row1, 0.5 * pad, ND, width, upper_color_limit_hex, 1.0)
    sankey_bar(ax_true_false, row1, -0.5 * pad, D, width, lower_color_limit_hex, 1.0)

    sankey_label(
        ax_true_false,
        row1,
        -0.5 * pad,
        -D,
        "Drought Predicted\n" + str(round(D, 1)) + "%",
        "right",
        -width,
    )
    sankey_label(
        ax_true_false,
        row1,
        0.5 * pad,
        ND,
        "No Drought Predicted\n" + str(round(ND, 1)) + "%",
        "right",
        -width,
    )

    # row 2
    sankey_bar(
        ax_true_false, row2, -2.0 * pad - D_ND, D_D, width, lower_color_limit_hex, 1.0
    )
    sankey_bar(ax_true_false, row2, -1.0 * pad, D_ND, width, ratio_3, 1.0)
    sankey_bar(ax_true_false, row2, 1.0 * pad, ND_D, width, ratio_3, 1.0)
    sankey_bar(
        ax_true_false, row2, 2.0 * pad + ND_D, ND_ND, width, upper_color_limit_hex, 1.0
    )

    sankey_label(
        ax_true_false,
        row2,
        -2.0 * pad - D_ND,
        -D_D,
        "Drought Obs.\n" + str(round(D_D, 1)) + "%",
        "right",
        -width,
    )
    sankey_label(
        ax_true_false,
        row2,
        -1.0 * pad,
        -D_ND,
        "No Drought Obs.\n" + str(round(D_ND, 1)) + "%",
        "right",
        -width,
    )
    sankey_label(
        ax_true_false,
        row2,
        1.0 * pad,
        ND_D,
        "Drought Obs.\n" + str(round(ND_D, 1)) + "%",
        "right",
        -width,
    )
    sankey_label(
        ax_true_false,
        row2,
        2.0 * pad + ND_D,
        ND_ND,
        "No Drought Obs.\n" + str(round(ND_ND, 1)) + "%",
        "right",
        -width,
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
        ratio_3,
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
    )

    sankey_swoop(ax_true_false, row1, row2, width, 0.5 * pad, pad, ND_D, ratio_3)
    sankey_swoop(
        ax_true_false,
        row1,
        row2,
        width,
        0.5 * pad + ND_D,
        2.0 * pad + ND_D,
        ND_ND,
        upper_color_limit_hex,
    )

    ax_true_false.set_xlim(-5)
    ax_true_false.set_axis_off()

    # make svg
    fig_true_false.savefig(
        "Task2/out/fc_tf_" + horizons[i] + "_desktop.png", dpi=400, metadata=None
    )
    fig_true_false.savefig(
        "Task2/out/fc_tf_" + horizons[i] + "_desktop.svg",
        dpi=150,
        metadata=None,
    )

    # remove metadata
    remove_metadata_and_fix(
        "Task2/out/fc_tf_" + horizons[i] + "_desktop.svg",
        "src/assets/svgs/fc_tf_" + horizons[i] + "_desktop.svg",
    )

    # to make the mobile version, we first adjust the figure size to a more horizontal aspect
    fig_true_false.set_size_inches(
        target_plotwidth_in_mobile,
        target_plotwidth_in_mobile / aspect_single_plot,
    )

    # make svg
    fig_true_false.savefig(
        "Task2/out/fc_tf_" + horizons[i] + "_mobile.svg", metadata=None
    )

    # remove metadata
    remove_metadata_and_fix(
        "Task2/out/fc_tf_" + horizons[i] + "_mobile.svg",
        "src/assets/svgs/fc_tf_" + horizons[i] + "_mobile.svg",
    )

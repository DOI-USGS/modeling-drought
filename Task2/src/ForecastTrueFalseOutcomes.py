### Import Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Task_config.defaults import *
from Task_config.functions import *
from Task_config.parameters import *

# compute rights and wrongs
horizon_weeks = tf_d["horizon"]

total_false = tf_d["false_neg"] + tf_d["false_pos"]
total_true = tf_d["true_pos"] + tf_d["true_neg"]
total_yes_drought = tf_d["true_pos"] + tf_d["false_pos"]
total_no_drought = tf_d["false_neg"] + tf_d["true_neg"]
total = total_yes_drought + total_no_drought

right_list = total_true / total * 100.0
wrong_list = total_false / total * 100.0

true_neg_list = tf_d["true_neg"] / total_no_drought * 100.0
false_neg_list = tf_d["false_neg"] / total_no_drought * 100.0

true_pos_list = tf_d["true_pos"] / total_yes_drought * 100.0
false_pos_list = tf_d["false_pos"] / total_yes_drought * 100.0


def bar_outcomes(title, lower_bar, lower_color, upper_bar, upper_color, suffix):
    # make figure
    fig_true_false = plt.figure(
        1,
        figsize=(
            target_single_plotwidth,
            target_single_plotwidth / aspect_single_plot,
        ),
        gid="figure-" + basename_gid_true_false_summary + "-" + suffix,
    )
    # add axes for the forecast
    ax_true_false = fig_true_false.add_axes(
        [0.1, 0.15, 0.85, 0.7],
        gid="axis-" + basename_gid_true_false_summary + "-" + suffix,
    )

    # plot for each day
    for i in range(0, len(tf_d)):
        # lower bar
        ax_true_false.fill_between(
            [i + label_pad, i + 1 - label_pad],
            [lower_bar[i], lower_bar[i]],
            [0.0, 0.0],
            facecolor=lower_color,
        )
        # upper bar
        ax_true_false.fill_between(
            [i + label_pad, i + 1 - label_pad],
            [lower_bar[i], lower_bar[i]],
            [lower_bar[i] + upper_bar[i], lower_bar[i] + upper_bar[i]],
            facecolor=upper_color,
        )

    # set axes parameters
    ax_true_false.set_ylim(0, 100)
    ax_true_false.set_yticks(
        [0.0, 20.0, 40.0, 60.0, 80.0, 100], ["0%", "20%", "40%", "60%", "80%", "100%"]
    )
    ax_true_false.set_xticks(
        np.linspace(1, 13, 13) - 0.5, [str(i) for i in range(1, 14)]
    )
    ax_true_false.set_title(
        title,
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

    # save plots
    save_desktop_mobile_tablet(
        dir_1="Task2/out/",
        dir_2="src/assets/svgs/",
        base_name="fc_tf_sum_" + suffix,
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

    plt.close()


bar_outcomes(
    title="All model outcomes",
    lower_bar=right_list,
    lower_color=ratio_7,
    upper_bar=wrong_list,
    upper_color=ratio_3,
    suffix="rw",
)

bar_outcomes(
    title="When neither severe nor extreme\nstreamflow drought is predicted",
    lower_bar=true_neg_list,
    lower_color=upper_color_limit_hex,
    upper_bar=false_neg_list,
    upper_color=upper_color_limit_hex_half_alpha,
    suffix="nd",
)

bar_outcomes(
    title="When severe nor extreme\nstreamflow drought is predicted",
    lower_bar=true_pos_list,
    lower_color=lower_color_limit_hex,
    upper_bar=false_pos_list,
    upper_color=lower_color_limit_hex_half_alpha,
    suffix="yd",
)

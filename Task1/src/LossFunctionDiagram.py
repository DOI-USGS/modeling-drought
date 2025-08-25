### Import Libraries
import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy import stats
from Task_config.defaults import *
from Task_config.functions import *
from Task_config.parameters import *

desktop_shrink = 0.9
desktop_height = 0.75
desktop_width = 0.275 * desktop_shrink
desktop_left = [0.05, 0.39, 0.73]
desktop_bottom = 0.15
### Plotting

# make figure
fig = plt.figure(
    1,
    figsize=(
        target_plotwidth_in_desktop,
        target_plotwidth_in_desktop / aspect_double_plot_desktop * desktop_shrink,
    ),
)
# add axes for loss function
ax_LF_1 = fig.add_axes(
    [desktop_left[0], desktop_bottom, desktop_width, desktop_height],
)
# add axes for loss function
ax_LF_2 = fig.add_axes(
    [desktop_left[1], desktop_bottom, desktop_width, desktop_height],
)
# add axes for loss function
ax_LF_3 = fig.add_axes(
    [desktop_left[2], desktop_bottom, desktop_width, desktop_height],
)

# loss function axis parameters
percentiles = [0.5, 1.0 - min_percentile, min_percentile]
for i, ax_LF in enumerate([ax_LF_1, ax_LF_2, ax_LF_3]):

    # plot the loss function
    ax_LF.plot(
        x_LF,
        pinball_LF(x_LF, 0.0, percentiles[i]),
        color=LFCMap(adjust(percentiles[i])),
        alpha=1.0,
        zorder=5,
    )

    ### Loss Function Plot
    # Add static loss function lines
    ax_LF.plot(
        x_LF,
        pinball_LF(x_LF, 0.0, min_percentile),
        color=np.array(lower_color_limit) / 256.0,
        linestyle="--",
        alpha=static_alpha,
    )
    ax_LF.plot(
        x_LF,
        pinball_LF(x_LF, 0.0, 0.5),
        color=median_color_hex,
        zorder=0,
        linestyle="--",
        alpha=static_alpha,
    )
    ax_LF.plot(
        x_LF,
        pinball_LF(x_LF, 0.0, 1.0 - min_percentile),
        color=np.array(upper_color_limit) / 256.0,
        linestyle="--",
        alpha=static_alpha,
    )
    # Fill between the lower and upper bounds
    ax_LF.fill_between(
        x_LF,
        pinball_LF(x_LF, 0.0, min_percentile),
        pinball_LF(x_LF, 0.0, 1.0 - min_percentile),
        color="tab:gray",
        alpha=fill_alpha,
        edgecolor="none",
    )
    # Add popup loss function lines
    ax_LF.plot(
        x_LF,
        pinball_LF(x_LF, 0.0, min_percentile),
        color=np.array(lower_color_limit) / 256.0,
        alpha=0.0,
        zorder=2,
    )
    ax_LF.plot(
        x_LF,
        pinball_LF(x_LF, 0.0, 0.5),
        color=median_color_hex,
        alpha=0.0,
        zorder=2,
    )
    ax_LF.plot(
        x_LF,
        pinball_LF(x_LF, 0.0, 1.0 - min_percentile),
        color=np.array(upper_color_limit) / 256.0,
        alpha=0.0,
        zorder=2,
    )

    ax_LF.tick_params(direction="out")
    ax_LF.set_ylim(0, 1)
    ax_LF.set_xlim(-1, 1)
    ax_LF.set_xticks(x_LF, ["Lower", "Median", "Upper"])
    ax_LF.set_yticks([0, 0.5, 1.0], ["Less\nPenalty\n", "", "More\nPenalty"])
    ax_LF.set_title("Loss function", loc="left", weight="extra bold", color="k")
    ax_LF.set_xlabel("Estimate", weight="semibold")
    ax_LF.spines["top"].set_visible(False)
    ax_LF.spines["right"].set_visible(False)

# save plots
mobile_height_mod = 1.5
mobile_height = 0.333 / mobile_height_mod
mobile_width = 0.8
mobile_left = 0.14
mobile_bottom = [0.07, 0.40, 0.73]

tablet_height_mod = 1.5
tablet_height = 0.375 / tablet_height_mod
tablet_width = 0.825
tablet_left = 0.125
tablet_bottom = [0.04, 0.38, 0.72]

save_desktop_mobile_tablet(
    dir_1="Task1/out/",
    dir_2="src/assets/svgs/",
    base_name="lf_diagram",
    fig=fig,
    mobile_dimensions=[
        target_plotwidth_in_mobile,
        target_plotwidth_in_mobile / aspect_double_plot_mobile * mobile_height_mod,
    ],
    tablet_dimensions=[
        target_plotwidth_in_tablet,
        target_plotwidth_in_tablet / aspect_double_plot_tablet * mobile_height_mod,
    ],
    mod_ax_list=[ax_LF_1, ax_LF_2, ax_LF_3],
    mobile_pos_list=[
        [mobile_left, mobile_bottom[2], mobile_width, mobile_height],
        [mobile_left, mobile_bottom[1], mobile_width, mobile_height],
        [mobile_left, mobile_bottom[0], mobile_width, mobile_height],
    ],
    tablet_pos_list=[
        [tablet_left, tablet_bottom[2], tablet_width, tablet_height],
        [tablet_left, tablet_bottom[1], tablet_width, tablet_height],
        [tablet_left, tablet_bottom[0], tablet_width, tablet_height],
    ],
)

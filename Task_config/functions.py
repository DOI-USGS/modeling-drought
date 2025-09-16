### Import Libraries
import numpy as np
import re
from scipy import stats
import matplotlib as mpl

# from Task_config.parameters import *

# from Task_config.defaults import *


# Custom Colormap
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def make_color_ramp(colors):
    # convert hex to rgb 8-bit
    lower_color_limit = hex_to_rgb(colors["lower_color_limit_hex"])
    upper_color_limit = hex_to_rgb(colors["upper_color_limit_hex"])
    median_color = hex_to_rgb(colors["median_color_hex"])

    vals = np.ones((256, 4))
    for i in range(0, 3):
        vals[:128, i] = np.linspace(
            lower_color_limit[i] / 256, median_color[i] / 256, 128
        )
        vals[128:, i] = np.linspace(
            median_color[i] / 256, upper_color_limit[i] / 256, 128
        )
    return mpl.colors.ListedColormap(vals)


# rescales the min to max percentile from 0 to 1
def adjust(percentile, min_percentile):
    return (percentile - min_percentile) / (1.0 - 2.0 * min_percentile)


# get asymmetric laplace distribution
def laplace(loc, scale, kappa, min_percentile):

    # find lower, upper, and median of asymmetric laplace distribution
    z_val_min = stats.laplace_asymmetric.ppf(
        min_percentile, kappa=kappa, loc=loc, scale=scale
    )
    z_val_max = stats.laplace_asymmetric.ppf(
        1.0 - min_percentile, kappa=kappa, loc=loc, scale=scale
    )
    if kappa < 1.0:
        z_median = loc - 1.0 / (kappa * scale) * np.log((1.0 + kappa**2.0) / (2.0))
    else:
        z_median = loc + kappa / scale * np.log((1.0 + kappa**2.0) / (2.0 * kappa**2.0))

    # loss function, x
    x_LF = np.array([-1.0, 0.0, 1.0])

    return z_val_min, z_val_max, z_median, x_LF


# draw pinball loss funcions
def pinball_LF(x_LF, real_value, quantile):
    y_LF = np.zeros_like(x_LF)
    for i in range(0, len(x_LF)):
        if x_LF[i] <= real_value:
            y_LF[i] = (real_value - float(x_LF[i])) * quantile
        else:
            y_LF[i] = (float(x_LF[i]) - real_value) * (1.0 - quantile)
    return y_LF


# truncate data and scale from 0 to 100
def forecast_format(y):
    # truncate 0
    y = np.maximum(np.zeros_like(y), y)
    # truncate 1
    y = np.minimum(np.ones_like(y) * 100.0, y)
    return y


# remove annoying metadata that sets vue warnings off
def remove_metadata_and_fix(infile, outfile):
    with open(infile, "r", encoding="utf-8") as input_file:
        input_content = input_file.read()

    # Remove <metadata> sections
    modified_content = re.sub(
        r"<metadata>.*?</metadata>\n?", "", input_content, flags=re.DOTALL
    )

    # Convert pt to px
    # This is a required workaround because Matplotlib correctly sizes the image based on the dpi and 72 points per inch
    # However, it incorrectly write the text as px, despite it actually being the size in pts (some weird scaling?)
    # By simply changing the size of the canvas as px instead of pt. Everything should be fixed.
    # NOTE: For this to work font must be specified in pixels, despite matplotlib documentation saying it's in points.
    modified_content = modified_content.replace("pt", "px")

    with open(outfile, "w", encoding="utf-8") as output_file:
        output_file.write(modified_content)


# create text in the svg that's meant to become opaque when something happens
def popup_text(ax, x, y, label, fontcolor, facecolor, edgecolor, va, ha, gid):
    ax.text(
        x,
        y,
        label,
        fontweight="bold",
        color=fontcolor,
        va=va,
        ha=ha,
        gid=gid + "-BOLD",
        transform=ax.transAxes,
        bbox=dict(facecolor="w", alpha=0.0000001, edgecolor="none", pad=0.0),
        zorder=2,
        alpha=0.0,
    )


# sankey bar
def sankey_bar(ax, xloc, yloc, height, width, color, alpha, gid=""):
    if yloc >= 0.0:
        ax.fill_between(
            [xloc - width * 0.5, xloc + width * 0.5],
            [yloc + height, yloc + height],
            [yloc, yloc],
            color=color,
            linewidth=0.0,
            alpha=alpha,
            gid=gid,
        )
    else:
        ax.fill_between(
            [xloc - width * 0.5, xloc + width * 0.5],
            [yloc, yloc],
            [yloc - height, yloc - height],
            color=color,
            linewidth=0.0,
            alpha=alpha,
            gid=gid,
        )


# sankey label
def sankey_label(ax, xloc, yloc, height, label, ha, pad, alpha=1.0, gid=""):
    ax.text(
        xloc + pad, yloc + height / 2.0, label, ha=ha, va="center", alpha=alpha, gid=gid
    )


# sankey swoop
def sankey_swoop(ax, x1, x2, width, y1, y2, height, color, alpha=0.2, gid=""):
    sigmoid_swoopiness = 2.0
    x_mid = (x1 + x2) / 2.0

    points = 100
    x = np.linspace(x1 + 0.5 * width, x2 - 0.5 * width, 100)
    y_lower = y1 + (y2 - y1) * (1.0 / (1.0 + np.exp(-sigmoid_swoopiness * (x - x_mid))))
    y_upper = y_lower + height
    ax.fill_between(x, y_lower, y_upper, color=color, alpha=alpha, linewidth=0, gid=gid)


def save_desktop_mobile_tablet(
    dir_1,
    dir_2,
    base_name,
    fig,
    mobile_dimensions,
    tablet_dimensions,
    mod_ax_list=None,
    mobile_pos_list=None,
    tablet_pos_list=None,
    text_obj=None,
    text_change=None,
    save_desktop=True,
    save_tablet=True,
    save_mobile=True,
):

    if save_desktop == True:
        # save desktop version
        fig.savefig(dir_1 + base_name + "_desktop.svg", dpi=150, metadata=None)

        # remove metadata
        remove_metadata_and_fix(
            dir_1 + base_name + "_desktop.svg",
            dir_2 + base_name + "_desktop.svg",
        )

    # change text if needed
    if text_obj != None:
        text_obj.set_text(text_change)

    if save_mobile == True:
        # to make the mobile version, we first adjust the figure size to a more horizontal aspect
        fig.set_size_inches(mobile_dimensions)
        if mobile_pos_list != None:
            for i, mod_ax in enumerate(mod_ax_list):
                mod_ax.set_position(mobile_pos_list[i])

        # make svg
        fig.savefig(dir_1 + base_name + "_mobile.svg", dpi=150, metadata=None)

        # remove metadata
        remove_metadata_and_fix(
            dir_1 + base_name + "_mobile.svg",
            dir_2 + base_name + "_mobile.svg",
        )

    if save_tablet == True:
        # to make the tablet version, we first adjust the figure size to a more horizontal aspect
        fig.set_size_inches(tablet_dimensions)
        if tablet_pos_list != None:
            for i, mod_ax in enumerate(mod_ax_list):
                mod_ax.set_position(tablet_pos_list[i])

        # make svg
        fig.savefig(dir_1 + base_name + "_tablet.svg", dpi=150, metadata=None)

        # remove metadata
        remove_metadata_and_fix(
            dir_1 + base_name + "_tablet.svg",
            dir_2 + base_name + "_tablet.svg",
        )


def set_axis_up(ax):
    ax.tick_params(direction="out")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_axisbelow(True)


def forecast_annotations(
    ax, labels, xys, xy_texts, target_fontsize_px, color, gid_prefix, ha="left"
):
    fontsizes = [
        target_fontsize_px,
        0.8 * target_fontsize_px,
        0.8 * target_fontsize_px,
    ]
    gid_suffix = ["", "-tablet", "-mobile"]
    for i, label in enumerate(labels):
        ax.annotate(
            label,
            color=color,
            va="center",
            fontsize=fontsizes[i],
            ha=ha,
            xy=xys[i],
            xytext=xy_texts[i],
            arrowprops=dict(
                facecolor=color,
                edgecolor=color,
                alpha=0.00001,
                arrowstyle="fancy",
                gid=gid_prefix + "-arrow" + gid_suffix[i],
            ),
            gid=gid_prefix + gid_suffix[i],
            alpha=0.0,
            zorder=100,
        )

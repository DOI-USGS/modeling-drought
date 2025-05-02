### Import Libraries
import numpy as np
import re
from Task_config.parameters import *
from Task_config.defaults import *


# rescales the min to max percentile from 0 to 1
def adjust(percentile):
    return (percentile - min_percentile) / (1.0 - 2.0 * min_percentile)


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
    with open(infile, "r") as input_file:
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

    with open(outfile, "w") as output_file:
        output_file.write(modified_content)


def selectable_text(ax, x, y, label, fontcolor, facecolor, edgecolor, va, ha, gid):
    text = ax.text(
        x,
        y,
        label,
        color=fontcolor,
        va=va,
        ha=ha,
        gid=gid,
        transform=ax.transAxes,
        bbox=dict(
            facecolor=facecolor,
            boxstyle="round",
            alpha=1,
            edgecolor=edgecolor,
            pad=button_padding,
            linewidth=0.75,
        ),
        zorder=1,
    )

    ax.text(
        x + shadow_offset_x,
        y + shadow_offset_y,
        label,
        color=shadow_color,
        va=va,
        ha=ha,
        gid="shadow-" + gid,
        transform=ax.transAxes,
        bbox=dict(
            facecolor=shadow_color,
            boxstyle="round",
            alpha=1,
            edgecolor=shadow_color,
            pad=button_padding,
            linewidth=0.75,
        ),
        zorder=0,
    )
    return text.get_window_extent().transformed(ax.transData.inverted())


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

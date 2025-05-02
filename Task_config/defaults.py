import os
import numpy as np
import matplotlib as mpl
import matplotlib.font_manager as font_manager

# Set default font size
target_fontsize_px = 16  # in px
target_fontsize_px_title = 20  # in px
# These are the target widths on the website.
target_single_plotwidth_px = 700
target_plotwidth_px_mobile = 400
target_plotwidth_px_tablet = 700
target_plotwidth_px_desktop = 1200
matplotlib_error_correction = 72  # matplotlib works in pt, but svg comes out in px. This fixes things with the remove_metadata_and_fix function.
target_single_plotwidth = target_single_plotwidth_px / matplotlib_error_correction
target_plotwidth_in_mobile = target_plotwidth_px_mobile / matplotlib_error_correction
target_plotwidth_in_tablet = target_plotwidth_px_tablet / matplotlib_error_correction
target_plotwidth_in_desktop = target_plotwidth_px_desktop / matplotlib_error_correction
aspect_single_plot = 1.333
aspect_double_plot_mobile = 0.8
aspect_double_plot_tablet = 1.0
aspect_double_plot_desktop = 3.0

# Shades of Gray
ratio_7 = "#595959"
ratio_5 = "#6E6E6E"
ratio_3 = "#949494"
ratio_1_5 = "#D1D1D1"

# adjust
font_manager.weight_dict.update({"light": 300})

mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["font.sans-serif"] = "Source Sans 3"  # prop.get_name()
mpl.rcParams["font.weight"] = "light"
mpl.rcParams["font.size"] = target_fontsize_px
mpl.rcParams["text.color"] = ratio_7
mpl.rcParams["axes.titlesize"] = target_fontsize_px_title
mpl.rcParams["axes.labelcolor"] = ratio_7
mpl.rcParams["xtick.labelcolor"] = ratio_7
mpl.rcParams["ytick.labelcolor"] = ratio_7
mpl.rcParams["xtick.color"] = ratio_3
mpl.rcParams["ytick.color"] = ratio_3
mpl.rcParams["axes.edgecolor"] = ratio_3
mpl.rcParams["grid.color"] = ratio_1_5

# Allow Text to be highlighted in SVG
mpl.rcParams["svg.fonttype"] = "none"

# Set default linewidth
mpl.rcParams["lines.linewidth"] = 1.0


# Custom Colormap
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


lower_color_limit_hex_half_alpha = "#DBC49A"
lower_color_limit_hex = "#B78935"
upper_color_limit_hex = "#406992"
upper_color_limit_hex_half_alpha = "#9FB4C8"
observation_color_hex = "#883e3a"
median_color_hex = "#00264c"

lower_color_limit = hex_to_rgb(lower_color_limit_hex)
upper_color_limit = hex_to_rgb(upper_color_limit_hex)
median_color = hex_to_rgb(median_color_hex)

vals = np.ones((256, 4))
for i in range(0, 3):
    vals[:128, i] = np.linspace(lower_color_limit[i] / 256, median_color[i] / 256, 128)
    vals[128:, i] = np.linspace(median_color[i] / 256, upper_color_limit[i] / 256, 128)
LFCMap = mpl.colors.ListedColormap(vals)

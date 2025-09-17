import os
from Task_config.functions import make_color_ramp
import matplotlib as mpl
import matplotlib.font_manager as font_manager
import yaml

with open("Task_config/parameters.yaml", "r") as file:
    params = yaml.safe_load(file)

# get yaml parameters
plotwidth = params["plotwidth"]
colors = params["colors"]
grays = params["grays"]
fontsize = params["fontsize"]

# Set default font size
target_fontsize_px = 16  # in px
target_fontsize_px_title = 20  # in px

# These are the target widths on the website.
target_single_plotwidth = (
    plotwidth["target_single_plotwidth_px"] / plotwidth["matplotlib_error_correction"]
)
target_plotwidth_in_mobile = (
    plotwidth["target_plotwidth_px_mobile"] / plotwidth["matplotlib_error_correction"]
)
target_plotwidth_in_tablet = (
    plotwidth["target_plotwidth_px_tablet"] / plotwidth["matplotlib_error_correction"]
)
target_plotwidth_in_desktop = (
    plotwidth["target_plotwidth_px_desktop"] / plotwidth["matplotlib_error_correction"]
)

# get color gradient from color pallette
LFCMap = make_color_ramp(colors)

# adjust the weight for light font weights
font_manager.weight_dict.update({"light": 300})

# set defaults in matplotlib
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["font.sans-serif"] = "Source Sans 3"
mpl.rcParams["font.weight"] = "light"
mpl.rcParams["font.size"] = fontsize["target_fontsize_px"]
mpl.rcParams["text.color"] = grays["ratio_9"]
mpl.rcParams["axes.titlesize"] = fontsize["target_fontsize_px_title"]
mpl.rcParams["axes.labelcolor"] = grays["ratio_9"]
mpl.rcParams["xtick.labelcolor"] = grays["ratio_9"]
mpl.rcParams["ytick.labelcolor"] = grays["ratio_9"]
mpl.rcParams["xtick.color"] = grays["ratio_3"]
mpl.rcParams["ytick.color"] = grays["ratio_3"]
mpl.rcParams["axes.edgecolor"] = grays["ratio_3"]
mpl.rcParams["grid.color"] = grays["ratio_1_5"]

# Allow Text to be highlighted in SVG
mpl.rcParams["svg.fonttype"] = "none"

# Set default linewidth
mpl.rcParams["lines.linewidth"] = params["linewidth"]

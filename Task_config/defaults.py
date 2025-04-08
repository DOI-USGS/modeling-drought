import os
import numpy as np
import matplotlib as mpl
import matplotlib.font_manager as font_manager

# Set default font size
target_fontsize_px = 16  # 12pt font
target_plotwidth_px_mobile = 700
target_plotwidth_px_desktop = 1200
default_viewport_px = 96
target_plotwidth_in_mobile = target_plotwidth_px_mobile / default_viewport_px
target_plotwidth_in_desktop = target_plotwidth_px_desktop / default_viewport_px
aspect_mobile = 1.0
aspect_desktop = 3.0

# Shades of Gray
ratio_7 = "#595959"
ratio_5 = "#6E6E6E"
ratio_3 = "#949494"
ratio_1_5 = "#D1D1D1"

# fonts
font_path = (
    os.getcwd() + "/Task_config/SourceSans3-VariableFont_wght.ttf"
)  # Your font path goes here
font_manager.fontManager.addfont(font_path)
prop = font_manager.FontProperties(fname=font_path)

mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["font.sans-serif"] = prop.get_name()
mpl.rcParams["font.weight"] = "light"
mpl.rcParams["font.size"] = 12
mpl.rcParams["text.color"] = ratio_7
mpl.rcParams["axes.labelcolor"] = ratio_7
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


lower_color_limit_hex = "#406992"
upper_color_limit_hex = "#B78935"
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

import os
import numpy as np
import matplotlib as mpl

# Load Universe Condensed Font
mpl.font_manager.fontManager.addfont(os.getcwd() + "/Task_Data/Univers-Condensed.otf")
prop = mpl.font_manager.FontProperties(
    fname=os.getcwd() + "/Task_Data/Univers-Condensed.otf"
)
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["font.sans-serif"] = [prop.get_name()]

# Set default font size
# mpl.rcParams['font.size'] = font_size_base = 8

# Allow Text to be highlighted in SVG
mpl.rcParams["svg.fonttype"] = "none"

# Set default linewidth
mpl.rcParams["lines.linewidth"] = 1.0

# Custom Colormap
lower_color_limit = [31, 119, 180]
upper_color_limit = [255, 127, 14]

vals = np.ones((256, 4))
for i in range(0, 3):
    vals[:128, i] = np.linspace(lower_color_limit[i] / 256, 0, 128)
    vals[128:, i] = np.linspace(0, upper_color_limit[i] / 256, 128)
LFCMap = mpl.colors.ListedColormap(vals)

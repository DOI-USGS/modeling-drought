import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime
from scipy import interpolate
import pyarrow.feather as feather
import re
import os

parent = os.getcwd()
mpl.font_manager.fontManager.addfont(parent + '/Task_Data/Univers-Condensed.otf')
prop = mpl.font_manager.FontProperties(fname= parent + '/Task_Data/Univers-Condensed.otf')
#mpl.rcParams['font.size'] = font_size_base = 8
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["font.sans-serif"] = [prop.get_name()]
mpl.rcParams['svg.fonttype'] = 'none'
mpl.rcParams['lines.linewidth'] = 1.0

tab_orange =  [255, 127, 14]
tab_blue = [31, 119, 180]

N = 256
vals = np.ones((N, 4))
for i in range (0,3):
    vals[:128, i] = np.linspace(tab_blue[i]/256, 0, 128)
    vals[128:, i] = np.linspace(0,tab_orange[i]/256, 128)
BBO_cmap = mpl.colors.ListedColormap(vals)

def adjust(percentile):
    return (percentile-min_percentile)/(1.0 - 2.0 * min_percentile)

# user parameters
number_of_frames = 501
min_percentile = 0.05
forecast_data = feather.read_feather("Task_Data/ForJeffrey_7day_forecast.feather")
prediction = -1  # -1 is the final prediction
date_range = ['2017-07-03','2019-07-01']
river_label = 'Colorado River Near Colorado-Utah State Line - 09163500'

# asymmetric laplace distribution parameters
# https://en.wikipedia.org/wiki/Asymmetric_Laplace_distribution
loc = 0.0
scale = 1.0
kappa = 0.5

# functions
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
    y = np.minimum(np.ones_like(y), y)
    # scale to 0 to 100
    y *= 100.0
    return y


# remove annoying metadata that sets vue warnings off
def remove_metadata(infile, outfile):
    output = open(outfile, "w")
    input = open(infile).read()
    output.write(re.sub("<metadata>.*?</metadata>\n", "", input, flags=re.DOTALL))
    output.close()

# make figure
fig = plt.figure(1, figsize=(10, 4),gid= 'figure-lossfunction')
# add axes
ax_LF = fig.add_axes([0.1, 0.175, 0.25, 0.75],gid= 'axis-lossfunction1')
ax_forecast = fig.add_axes([0.425, 0.175, 0.45, 0.75],gid= 'axis-lossfunction2')

ax_LF.annotate('Drag mouse over\ngray region',fontweight='bold', va = 'center',ha='center',xy=(-.8,0.1), xytext=(-0.1,0.65),arrowprops=dict(facecolor='black', gid='annotation_lossfunction_arrow',arrowstyle='fancy',connectionstyle='arc3,rad=0.3',alpha=0.8),zorder=10,gid='annotation_lossfunction')

# loss function x-array
x_LF = np.array([-1.0, 0.0, 1.0])

# load date data
x_forecast_raw = forecast_data["datetime"].values.astype('datetime64[D]')

#get bounds
lower_bound = np.argmin(np.abs(x_forecast_raw-np.datetime64(date_range[0])))
upper_bound = np.argmin(np.abs(x_forecast_raw-np.datetime64(date_range[1])))+1

#cut data
x_forecast = x_forecast_raw[lower_bound:upper_bound]

# load observed data
y_training = forecast_data["observed"][lower_bound:upper_bound]

# load model data
y_forecast_lower = forecast_format(
    forecast_data["lower"][lower_bound:upper_bound]/100.
)
y_forecast_median = forecast_format(
    forecast_data["median"][lower_bound:upper_bound]/100.
)
y_forecast_upper = forecast_format(
    forecast_data["upper"][lower_bound:upper_bound]/100.
)

# find lower, upper and median of ALD
z_val_min = sp.stats.laplace_asymmetric.ppf(
    min_percentile, kappa=kappa, loc=loc, scale=scale
)
z_val_max = sp.stats.laplace_asymmetric.ppf(
    1.0 - min_percentile, kappa=kappa, loc=loc, scale=scale
)
if kappa < 1.0:
    z_median = loc - 1.0 / (kappa * scale) * np.log((1.0 + kappa**2.0) / (2.0))
else:
    z_median = loc + kappa / scale * np.log((1.0 + kappa**2.0) / (2.0 * kappa**2.0))

# generate lines based on percentile
for i, percentile in enumerate(
    np.linspace(min_percentile, 1.0 - min_percentile, number_of_frames)
):
    # plot the loss function
    ax_LF.plot(
        x_LF,
        pinball_LF(x_LF, 0.0, percentile),
        color=BBO_cmap(adjust(percentile)),
        gid="LF-" + str(i),
        alpha=0.0,
        zorder=5
    )

    # calculate the corresponding z value
    z_val = sp.stats.laplace_asymmetric.ppf(
        percentile, kappa=kappa, loc=loc, scale=scale
    )
    # calculate the forecast line
    if percentile < 0.50:
        y_forecast_temp = y_forecast_median + (y_forecast_lower - y_forecast_median) * (
            z_val - z_median
        ) / (z_val_min - z_median)
    else:
        y_forecast_temp = y_forecast_median + (y_forecast_upper - y_forecast_median) * (
            z_val - z_median
        ) / (z_val_max - z_median)

    # plot the forecast line
    ax_forecast.plot(
        x_forecast, y_forecast_temp, color=BBO_cmap(adjust(percentile)), gid="FORECAST-" + str(i), alpha=0.0,
        zorder=5
    )

static_alpha = 0.25
fill_alpha = 0.15
# Add static loss function lines
ax_LF.plot(x_LF, pinball_LF(x_LF, 0.0, min_percentile), color="tab:blue", linestyle="--",alpha=static_alpha)
ax_LF.plot(x_LF, pinball_LF(x_LF, 0.0, 0.5), color="k", zorder=0, linestyle="--",alpha=static_alpha)
ax_LF.plot(x_LF,pinball_LF(x_LF, 0.0, 1.0 - min_percentile),color="tab:orange",linestyle="--",alpha=static_alpha)
# Add Popup loss function lines
ax_LF.plot(x_LF, pinball_LF(x_LF, 0.0, min_percentile), color="tab:blue", alpha=0.0, zorder=2, gid = "LOWER-LF-LINE")
ax_LF.plot(x_LF, pinball_LF(x_LF, 0.0, 0.5), color="k", alpha=0.0, zorder=2, gid = "MEDIAN-LF-LINE")
ax_LF.plot(x_LF,pinball_LF(x_LF, 0.0, 1.0 - min_percentile),color="tab:orange", alpha=0.0, zorder=2, gid = "UPPER-LF-LINE")
# Fill between the lower and upper bounds
ax_LF.fill_between(x_LF,pinball_LF(x_LF, 0.0, min_percentile), pinball_LF(x_LF, 0.0, 1.0 - min_percentile),color="tab:gray",alpha=fill_alpha,edgecolor='none')
# loss function axis parameters
ax_LF.tick_params(direction="out")
ax_LF.set_ylim(0, 1)
ax_LF.set_xlim(-1, 1)
ax_LF.set_xticks(x_LF, ["Lower", "Median", "Uppper"])
ax_LF.get_yaxis().set_ticks([0, 0.5, 1.0], ["Less\nPenalty\n", "", "More\nPenalty"])
ax_LF.set_xlabel("Estimate")
ax_LF.set_title("Loss Function", loc="left",weight='bold')
ax_LF.spines["top"].set_visible(False)
ax_LF.spines["right"].set_visible(False)

# add static forecast lines
ax_forecast.plot(x_forecast, y_forecast_lower, color="tab:blue", linestyle="--",alpha=static_alpha)
ax_forecast.plot(x_forecast, y_forecast_median, color="k", linestyle="--",alpha=static_alpha)
ax_forecast.plot(x_forecast, y_forecast_upper, color="tab:orange", linestyle="--",alpha=static_alpha)
# add popup forecast lines
ax_forecast.plot(x_forecast, y_training, color="tab:red",alpha=0.0,gid='observation-full-lf')
ax_forecast.plot(x_forecast, y_forecast_lower, color="tab:blue", alpha=0.0, zorder=2, gid = "LOWER-FORECAST-LINE")
ax_forecast.plot(x_forecast, y_forecast_median, color="k", alpha=0.0, zorder=2, gid = "MEDIAN-FORECAST-LINE")
ax_forecast.plot(x_forecast, y_forecast_upper, color="tab:orange", alpha=0.0, zorder=2, gid = "UPPER-FORECAST-LINE")
#fill between upper and lower
ax_forecast.fill_between(x_forecast,y_forecast_lower,y_forecast_upper,color="tab:gray",alpha=fill_alpha,edgecolor='none')

# add labels for the prediction quantiles
# convert to timestamp, hours
labels_bump = 1.01
lower_interp = interpolate.interp1d(x_forecast.astype(float),y_forecast_lower,kind='linear')
median_interp = interpolate.interp1d(x_forecast.astype(float),y_forecast_median,kind='linear')
upper_interp = interpolate.interp1d(x_forecast.astype(float),y_forecast_upper,kind='linear')

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

def selectable_text(ax,x,y,label,color,va,ha,gid):
    shadow_color = (0.4,0.4,0.4)
    shadow_offset_x = 0.004
    shadow_offset_y = -0.005
    if color == 'k':
        text = ax.text(x,y,label,color='w',va=va,ha=ha,gid=gid,transform=ax_forecast.transAxes,
            bbox=dict(facecolor=color,boxstyle='round', alpha=1, edgecolor=(0.6,0.6,0.6),pad=0.10,linewidth=0.75),zorder=1)
    else:
        text = ax.text(x,y,label,color='w',va=va,ha=ha,gid=gid,transform=ax_forecast.transAxes,
            bbox=dict(facecolor=color,boxstyle='round', alpha=1, edgecolor="k",pad=0.10,linewidth=0.75),zorder=1)
    ax.text(x+shadow_offset_x,y+shadow_offset_y,label,color=shadow_color,va=va,ha=ha,gid='shadow-'+gid,transform=ax_forecast.transAxes,
        bbox=dict(facecolor=shadow_color,boxstyle='round', alpha=1, edgecolor=shadow_color,pad=0.10,linewidth=0.75),zorder=0)
    return (text.get_window_extent().transformed(plt.gca().transData.inverted()))

# add textbox for lines. Need a fix, when alpha is zero, the box is not rendered in the svg. Bandaid is to make alpha very very small.
bbox1 = selectable_text(ax_forecast,labels_bump,lower_interp(np.datetime64(date_range[-1]).astype(float))/100.0,"5% Quantile","tab:blue","top","left","LOWER-TAG")
bbox2 = selectable_text(ax_forecast,labels_bump,median_interp(np.datetime64(date_range[-1]).astype(float))/100.0,"Median","k","center","left","MEDIAN-TAG")
bbox3 = selectable_text(ax_forecast,labels_bump,upper_interp(np.datetime64(date_range[-1]).astype(float))/100.0,"95% Quantile","tab:orange","bottom","left","UPPER-TAG")
bbox4 = selectable_text(ax_forecast,0.99,1.02, "Toggle Observations","tab:red","bottom","right","toggle-observations-lf")

button_label_loc = (0.75,0.9)
ax_forecast.annotate('Click & hover\nover buttons',fontweight='bold', va = 'center',ha='center',xy=(0.5*(bbox1.x0+bbox1.x1),bbox1.y1), xytext=button_label_loc,xycoords='axes fraction',arrowprops=dict(facecolor='black', gid='annotation_buttons1_arrow1', shrinkB=5,arrowstyle='->',connectionstyle='arc3,rad=-0.3',alpha=0.8),zorder=10,gid='annotation_buttons1')
ax_forecast.annotate('Click & hover\nover buttons',fontweight='bold', va = 'center',ha='center',xy=(0.5*(bbox2.x0+bbox2.x1),bbox2.y1), xytext=button_label_loc,xycoords='axes fraction',arrowprops=dict(facecolor='black', gid='annotation_buttons1_arrow2', shrinkB=5,arrowstyle='->',connectionstyle='arc3,rad=-0.3',alpha=0.8),zorder=10,alpha=0.0)
ax_forecast.annotate('Click & hover\nover buttons',fontweight='bold', va = 'center',ha='center',xy=(bbox3.x0,0.5*(bbox3.y0+bbox3.y1)), xytext=button_label_loc,xycoords='axes fraction',arrowprops=dict(facecolor='black', gid='annotation_buttons1_arrow3', shrinkB=5,arrowstyle='->',connectionstyle='arc3,rad=-0.3',alpha=0.8),zorder=10,alpha=0.0)
ax_forecast.annotate('Click & hover\nover buttons',fontweight='bold', va = 'center',ha='center',xy=(0.5*(bbox4.x0+bbox4.x1),bbox4.y0), xytext=button_label_loc,xycoords='axes fraction',arrowprops=dict(facecolor='black', gid='annotation_buttons1_arrow4', shrinkB=5,arrowstyle='->',connectionstyle='arc3,rad=-0.3',alpha=0.8),zorder=10,alpha=0.0)

# forecast axis parameters
ax_forecast.grid(visible=True, axis="y")
ax_forecast.tick_params(direction="out")
ax_forecast.set_ylim(0, 100.0)
ax_forecast.set_xlim(np.datetime64(date_range[0]),np.datetime64(date_range[-1]))
start_year = 1971 + np.datetime64(date_range[0],'Y').astype(int)
end_year = 1971 + np.datetime64(date_range[-1],'Y').astype(int)
x_ticks = [np.datetime64(str(i) + "-01-01") for i in range(start_year,end_year)]
x_ticks_labels = [i for i in range(start_year,end_year)]
ax_forecast.set_xticks(x_ticks,x_ticks_labels)
ax_forecast.set_yticks([0, 20, 40, 60, 80, 100], ["0%", "20%", "40%", "60%", "80%", "100%"])
ax_forecast.set_xlabel("Date")
ax_forecast.set_title("Streamflow Percentile", loc="left",weight='bold')
ax_forecast.spines["top"].set_visible(False)
ax_forecast.spines["right"].set_visible(False)
ax_forecast.set_axisbelow(True)

#river label
plt.figtext(1,0,river_label,ha='right',va='bottom',alpha=0.5)

#make svg
fig.savefig("Task1/out/lf_example.svg", dpi=150, metadata=None)

#remove metadata
remove_metadata("Task1/out/lf_example.svg", "src/assets/svgs/lf_example.svg")
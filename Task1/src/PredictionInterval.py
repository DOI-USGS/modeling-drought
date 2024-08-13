import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime
from scipy import interpolate
import pyarrow.feather as feather
import re
import os

# Get Parent Directory Path
parent = os.getcwd()

# Import Univers Condensed Font
mpl.font_manager.fontManager.addfont(parent + '/Task_Data/Univers-Condensed.otf')
prop = mpl.font_manager.FontProperties(fname= parent + '/Task_Data/Univers-Condensed.otf')

# Set Matplotlib Defaults
#mpl.rcParams['font.size'] = font_size_base = 8
mpl.rcParams["font.family"] = "sans-serif"
mpl.rcParams["font.sans-serif"] = [prop.get_name()]
mpl.rcParams['svg.fonttype'] = 'none'
mpl.rcParams['lines.linewidth'] = 1.0


# Viz Parameters
min_percentile = 0.05
date_range = ['2017-07-03','2019-07-01']
river_label = 'Colorado River Near Colorado-Utah State Line - 09163500'

# Viz Data
forecast_data = feather.read_feather("Task_Data/ForJeffrey_7day_forecast.feather")

# Asymmetric Laplace Distribution parameters
# https://en.wikipedia.org/wiki/Asymmetric_Laplace_distribution
loc = 0.0
scale = 1.0
kappa = 0.5

###### Functions ######
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
def remove_metadata(infile, outfile):
    output = open(outfile, "w")
    input = open(infile).read()
    output.write(re.sub("<metadata>.*?</metadata>\n", "", input, flags=re.DOTALL))
    output.close()

# make figure
fig = plt.figure(1, figsize=(10, 4), gid= 'figure-predictioninterval')

# add axes
ax_LF = fig.add_axes([0.1, 0.175, 0.25, 0.75])
ax_forecast = fig.add_axes([0.425, 0.175, 0.45, 0.75])

# loss function x-array
x_LF = np.array([-1.0, 0.0, 1.0])

# load date data
x_forecast = forecast_data["datetime"].values.astype('datetime64[D]')

# load observed data
y_training = forecast_data["observed"]

# load model data
y_forecast_lower = forecast_format(forecast_data["lower"])
y_forecast_median = forecast_format(forecast_data["median"])
y_forecast_upper = forecast_format(forecast_data["upper"])

# find lower, upper and median of ALD
z_val_min = sp.stats.laplace_asymmetric.ppf(min_percentile, kappa=kappa, loc=loc, scale=scale)
z_val_max = sp.stats.laplace_asymmetric.ppf(1.0 - min_percentile, kappa=kappa, loc=loc, scale=scale)
if kappa < 1.0:
    z_median = loc - 1.0 / (kappa * scale) * np.log((1.0 + kappa**2.0) / (2.0))
else:
    z_median = loc + kappa / scale * np.log((1.0 + kappa**2.0) / (2.0 * kappa**2.0))

# calculate start and end index of date range
start_index = end_index = -9999
for i, x_forecast_loc in enumerate(x_forecast):
    if x_forecast_loc >= np.datetime64(date_range[0]) and start_index == -9999:
        start_index = i
    if x_forecast_loc > np.datetime64(date_range[1]) and end_index == -9999:
        end_index = i

# generate lines based on percentile
pi_list = [0.05,0.125,0.25]
facecolor_list = [(0.9,0.9,0.9),(0.75,0.75,0.75),(0.5,0.5,0.5)]
lower_limit_pi =[]
inside_proportion = []
for i, lower_percentile in enumerate(pi_list):

    upper_percentile = 1.0 - lower_percentile
    # Add Popup loss function lines
    ax_LF.plot(x_LF, pinball_LF(x_LF, 0.0, lower_percentile), color="tab:blue", alpha=0.0, zorder=2, gid = "LF-LOWER-" + str(i))
    ax_LF.plot(x_LF,pinball_LF(x_LF, 0.0, upper_percentile),color="tab:orange", alpha=0.0, zorder=2, gid = "LF-UPPER-" + str(i))

    # calculate the corresponding z value
    z_val_lower = sp.stats.laplace_asymmetric.ppf(
        lower_percentile, kappa=kappa, loc=loc, scale=scale
    )
    z_val_upper = sp.stats.laplace_asymmetric.ppf(
        upper_percentile, kappa=kappa, loc=loc, scale=scale
    )
    # calculate the forecast line
    if lower_percentile < 0.50:
        y_forecast_temp_lower = y_forecast_median + (y_forecast_lower - y_forecast_median) * (
            z_val_lower - z_median
        ) / (z_val_min - z_median)
    else:
        y_forecast_temp_lower = y_forecast_median + (y_forecast_upper - y_forecast_median) * (
            z_val_lower - z_median
        ) / (z_val_max - z_median)

    if upper_percentile < 0.50:
        y_forecast_temp_upper = y_forecast_median + (y_forecast_lower - y_forecast_median) * (
            z_val_upper - z_median
        ) / (z_val_min - z_median)
    else:
        y_forecast_temp_upper = y_forecast_median + (y_forecast_upper - y_forecast_median) * (
            z_val_upper - z_median
        ) / (z_val_max - z_median)

    # plot the forecast line
    ax_forecast.fill_between(
        x_forecast, y_forecast_temp_lower, y_forecast_temp_upper, color=facecolor_list[i], gid="PI-PATCH-" + str(i), alpha=0.00001,edgecolor='none',zorder=0
    )
    ax_forecast.plot(x_forecast, y_forecast_temp_lower, color="tab:blue", gid="PI-PATCH-LOWER-" + str(i), alpha=0.0,zorder=0)
    ax_forecast.plot(x_forecast, y_forecast_temp_upper, color="tab:orange", gid="PI-PATCH-UPPER-" + str(i), alpha=0.0,zorder=0)

    #get coordiante of upper bounds at x_max limit
    lower_interp = interpolate.interp1d(x_forecast.astype(float),y_forecast_temp_lower,kind='linear')
    lower_limit_pi += [lower_interp(np.datetime64(date_range[-1]).astype(float))/100.0]

    #calculate what's inside
    inside_count = 0
    count = 0
    outside_count = 0

    missed_x = []
    missed_y = []
    for j in range(start_index,end_index):
        if y_forecast_temp_lower.values[j] <= y_training.values[j] and y_training.values[j] <= y_forecast_temp_upper.values[j]:
            inside_count += 1
        else:
            outside_count+=1
            missed_x += [j]
            missed_y += [y_training.values[j]]
        count += 1
    print (outside_count,lower_percentile,"PI-missed-" + str(i))
    inside_proportion += [float(inside_count)/float(count)]
    
    ax_forecast.plot(x_forecast[missed_x],missed_y,markersize=8.+float(i/200),alpha=0.0,marker='x',color='k',linestyle='-',gid="PI-missed-" + str(i),zorder=3)


# Add static loss function lines
ax_LF.plot(x_LF, pinball_LF(x_LF, 0.0, 0.5), color="k", zorder=0, alpha = 0.0, gid='LF-LOWER-MEDIAN')
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

# # add static forecast lines
ax_forecast.plot(x_forecast, y_forecast_median, color="k",gid='PI-PATCH-MEDIAN',alpha=0.0)
# # add popup forecast lines
ax_forecast.plot(x_forecast, y_training, color="tab:red", alpha=1.0, gid="OBSERVED-FORECAST-LINE",zorder=2)
# # dummy missed observations
ax_forecast.plot([0,1],[1,1],marker='x',color='k',linestyle='none',label='missed prediction')

# add labels for the prediction quantiles
labels_bump = 1.01
median_interp = interpolate.interp1d(x_forecast.astype(float),y_forecast_median,kind='linear')

def selectable_text(ax,x,y,label,fontcolor,facecolor,edgecolor,va,ha,gid,button):
    if button:
        ax.text(x,y,label,color=fontcolor,va=va,ha=ha,gid=gid,transform=ax_forecast.transAxes,
            bbox=dict(facecolor=facecolor,boxstyle='round', alpha=1, edgecolor=edgecolor,pad=0.10,linewidth=0.75),zorder=1)

        shadow_color = (0.4,0.4,0.4)
        shadow_offset_x = 0.004
        shadow_offset_y = -0.005
        text = ax.text(x+shadow_offset_x,y+shadow_offset_y,label,color=shadow_color,va=va,ha=ha,gid='shadow-'+gid,transform=ax_forecast.transAxes,
            bbox=dict(facecolor=shadow_color,boxstyle='round', alpha=1, edgecolor=shadow_color,pad=0.10,linewidth=0.75),zorder=0)
    else:
        text = ax.text(x,y,label,fontweight='bold',color=fontcolor,va=va,ha=ha,gid=gid+"-BOLD",transform=ax_forecast.transAxes,
        bbox=dict(facecolor="w", alpha=0.0000001, edgecolor="none", pad=0.0),zorder=2,alpha=0.0)
    return (text.get_window_extent().transformed(ax.transData.inverted()))

# add textbox for lines. Need a fix, when alpha is zero, the box is not rendered in the svg. Bandaid is to make alpha very very small.
va_list = ["top","center","bottom"]
button_label_loc = (0.75,0.9)
bbox = selectable_text(ax_forecast,labels_bump,median_interp(np.datetime64(date_range[-1]).astype(float))/100.0,"Median","w",'k',(0.6,0.6,0.6),"center","left","TAG-MEDIAN",True)
ax_forecast.annotate('Hover over\nbuttons',fontweight='bold', va = 'center',ha='center',xy=(bbox.x0,0.5*(bbox.y1+bbox.y0)), xytext=button_label_loc,xycoords='axes fraction',zorder=10,gid='annotation_buttons2',arrowprops=dict(facecolor='black', gid='annotation_buttons2_arrow1',arrowstyle='->', shrinkB=5,connectionstyle='arc3,rad=-0.3',alpha=0.8))
for i,pi in enumerate(pi_list):
    bbox = selectable_text(ax_forecast,labels_bump,lower_limit_pi[i],str(int(100. * (1.0 - 2.0 * pi)))+"% PI",'k',facecolor_list[i],'k',va_list[i],"left","TAG-" +str(i),True)
    selectable_text(ax_forecast,0.6,0.9, "PI Contains\n"+str(round(inside_proportion[i]*100.,1))+"% of Observations","tab:red",'NULL','NULL',"center","center","TAG-" + str(i) + "-LABEL",False)
    ax_forecast.annotate('Hover over\nbuttons',fontweight='bold', va = 'center',ha='center',alpha=0.0,xy=(bbox.x0,0.5*(bbox.y1+bbox.y0)), xytext=button_label_loc,xycoords='axes fraction',zorder=10,arrowprops=dict(facecolor='black', gid='annotation_buttons2_arrow'+str(i+2),arrowstyle='->', shrinkB=5,connectionstyle='arc3,rad=-0.3',alpha=0.8))

# forecast axis parameters
ax_forecast.grid(visible=True, axis="y")
ax_forecast.legend(loc='lower left',edgecolor='none')
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
fig.savefig("Task1/out/pi_example.svg", dpi=150, metadata=None)

#remove metadata
remove_metadata("Task1/out/pi_example.svg", "src/assets/svgs/pi_example.svg")
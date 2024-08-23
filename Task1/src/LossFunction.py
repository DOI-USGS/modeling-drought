### Import Libraries
import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy import stats
from scipy import interpolate
from defaults import *
from functions import *
from parameters import *

### Plotting

# make figure
fig = plt.figure(1, figsize=(10, 4), gid= 'figure-' + basename_gid_lf)
# add axes for loss function
ax_LF = fig.add_axes([0.1, 0.175, 0.25, 0.75], gid= 'axis-'+ basename_gid_lf+'1')
# add axes for the forecast
ax_forecast = fig.add_axes([0.425, 0.175, 0.45, 0.75],gid= 'axis-'+ basename_gid_lf+'2')

### Data Arrays

# loss function x-array
x_LF = np.array([-1.0, 0.0, 1.0])

# load date data
x_forecast_raw = forecast_data["datetime"].values.astype('datetime64[D]')

#get temporal bounds
lower_bound = np.argmin(np.abs(x_forecast_raw-np.datetime64(date_range[0])))
upper_bound = np.argmin(np.abs(x_forecast_raw-np.datetime64(date_range[1])))+1

#cut data
x_forecast = x_forecast_raw[lower_bound:upper_bound]

# load observed data
y_training = forecast_data["observed"][lower_bound:upper_bound]

# load model data (lower, median, and upper)
y_forecast_lower = forecast_format(forecast_data["lower"][lower_bound:upper_bound])
y_forecast_median = forecast_format(forecast_data["median"][lower_bound:upper_bound])
y_forecast_upper = forecast_format(forecast_data["upper"][lower_bound:upper_bound])

# generate lines based on percentile
for i, percentile in enumerate(np.linspace(min_percentile, 1.0 - min_percentile, number_of_frames_lf)):

    # plot the loss function
    ax_LF.plot(
        x_LF,
        pinball_LF(x_LF, 0.0, percentile),
        color=LFCMap(adjust(percentile)),
        gid="LF-" + str(i),
        alpha=0.0,
        zorder=5
    )

    # calculate the corresponding z value
    z_val = stats.laplace_asymmetric.ppf(
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
        x_forecast, y_forecast_temp, color=LFCMap(adjust(percentile)), gid="FORECAST-" + str(i), alpha=0.0,
        zorder=5
    )

# create interpolated line for lower, median, and upper lines - to locate the side buttons
lower_interp = interpolate.interp1d(x_forecast.astype(float),y_forecast_lower,kind='linear')
median_interp = interpolate.interp1d(x_forecast.astype(float),y_forecast_median,kind='linear')
upper_interp = interpolate.interp1d(x_forecast.astype(float),y_forecast_upper,kind='linear')

# add textbox for lines. Need a fix, when alpha is zero, the box is not rendered in the svg. Bandaid is to make alpha very very small.
bbox1 = selectable_text(ax_forecast,labels_bump,lower_interp(np.datetime64(date_range[-1]).astype(float))/100.0,"5% Quantile","w",np.array(lower_color_limit)/256.,"k","top","left","LOWER-TAG")
bbox2 = selectable_text(ax_forecast,labels_bump,median_interp(np.datetime64(date_range[-1]).astype(float))/100.0,"Median","w","k",(0.6,0.6,0.6),"center","left","MEDIAN-TAG")
bbox3 = selectable_text(ax_forecast,labels_bump,upper_interp(np.datetime64(date_range[-1]).astype(float))/100.0,"95% Quantile","k",np.array(upper_color_limit)/256.,"k","bottom","left","UPPER-TAG")
bbox4 = selectable_text(ax_forecast,0.99,1.02, "Toggle Observations","w","tab:red","k","bottom","right","toggle-observations-lf")

# annotations
ax_LF.annotate('Drag mouse over\ngray region',fontweight='bold', va = 'center',ha='center',xy=(-.8,0.1), xytext=(-0.1,0.65),arrowprops=dict(facecolor='black', gid='annotation_lossfunction_arrow',arrowstyle='fancy',connectionstyle='arc3,rad=0.3',alpha=0.8),zorder=10,gid='annotation_lossfunction')
ax_forecast.annotate('Click & hover\nover buttons',fontweight='bold', va = 'center',ha='center',xy=(0.5*(bbox1.x0+bbox1.x1),bbox1.y1), xytext=annotation_label_loc_lf,xycoords='axes fraction',arrowprops=dict(facecolor='black', gid='annotation_buttons1_arrow1', shrinkA = 8, shrinkB=10,arrowstyle='->',connectionstyle='arc3,rad=-0.3',alpha=0.8),zorder=10,gid='annotation_buttons1')
ax_forecast.annotate('Click & hover\nover buttons',fontweight='bold', va = 'center',ha='center',xy=(bbox2.x0,0.5*(bbox2.y0+bbox2.y1)), xytext=annotation_label_loc_lf,xycoords='axes fraction',arrowprops=dict(facecolor='black', gid='annotation_buttons1_arrow2', shrinkA = 12, shrinkB=10,arrowstyle='->',connectionstyle='arc3,rad=-0.3',alpha=0.8),zorder=10,alpha=0.0)
ax_forecast.annotate('Click & hover\nover buttons',fontweight='bold', va = 'center',ha='center',xy=(bbox3.x0,0.5*(bbox3.y0+bbox3.y1)), xytext=annotation_label_loc_lf,xycoords='axes fraction',arrowprops=dict(facecolor='black', gid='annotation_buttons1_arrow3', shrinkA = 10, shrinkB=10,arrowstyle='->',connectionstyle='arc3,rad=-0.3',alpha=0.8),zorder=10,alpha=0.0)
ax_forecast.annotate('Click & hover\nover buttons',fontweight='bold', va = 'center',ha='center',xy=(0.5*(bbox4.x0+bbox4.x1),bbox4.y0), xytext=annotation_label_loc_lf,xycoords='axes fraction',arrowprops=dict(facecolor='black', gid='annotation_buttons1_arrow4', shrinkA = 8, shrinkB=20,arrowstyle='->',connectionstyle='arc3,rad=-0.3',alpha=0.8),zorder=10,alpha=0.0)

### Loss Function Plot
# Add static loss function lines
ax_LF.plot(x_LF, pinball_LF(x_LF, 0.0, min_percentile), color=np.array(lower_color_limit)/256., linestyle="--",alpha=static_alpha)
ax_LF.plot(x_LF, pinball_LF(x_LF, 0.0, 0.5), color="k", zorder=0, linestyle="--",alpha=static_alpha)
ax_LF.plot(x_LF,pinball_LF(x_LF, 0.0, 1.0 - min_percentile),color=np.array(upper_color_limit)/256.,linestyle="--",alpha=static_alpha)
# Fill between the lower and upper bounds
ax_LF.fill_between(x_LF,pinball_LF(x_LF, 0.0, min_percentile), pinball_LF(x_LF, 0.0, 1.0 - min_percentile),color="tab:gray",alpha=fill_alpha,edgecolor='none')
# Add popup loss function lines
ax_LF.plot(x_LF, pinball_LF(x_LF, 0.0, min_percentile), color=np.array(lower_color_limit)/256., alpha=0.0, zorder=2, gid = "LOWER-LF-LINE")
ax_LF.plot(x_LF, pinball_LF(x_LF, 0.0, 0.5), color="k", alpha=0.0, zorder=2, gid = "MEDIAN-LF-LINE")
ax_LF.plot(x_LF,pinball_LF(x_LF, 0.0, 1.0 - min_percentile),color=np.array(upper_color_limit)/256., alpha=0.0, zorder=2, gid = "UPPER-LF-LINE")

# loss function axis parameters
ax_LF.tick_params(direction="out")
ax_LF.set_ylim(0, 1)
ax_LF.set_xlim(-1, 1)
ax_LF.set_xticks(x_LF, ["Lower", "Median", "Upper"])
ax_LF.get_yaxis().set_ticks([0, 0.5, 1.0], ["Less\nPenalty\n", "", "More\nPenalty"])
ax_LF.set_xlabel("Estimate")
ax_LF.set_title("Loss Function", loc="left",weight='bold')
ax_LF.spines["top"].set_visible(False)
ax_LF.spines["right"].set_visible(False)

### Forecast Plot
# add static forecast lines
ax_forecast.plot(x_forecast, y_forecast_lower, color=np.array(lower_color_limit)/256., linestyle="--",alpha=static_alpha)
ax_forecast.plot(x_forecast, y_forecast_median, color="k", linestyle="--",alpha=static_alpha)
ax_forecast.plot(x_forecast, y_forecast_upper, color=np.array(upper_color_limit)/256., linestyle="--",alpha=static_alpha)
# fill between upper and lower
ax_forecast.fill_between(x_forecast,y_forecast_lower,y_forecast_upper,color="tab:gray",alpha=fill_alpha,edgecolor='none')
# add popup forecast lines
ax_forecast.plot(x_forecast, y_training, color="tab:red",linestyle=obs_linestyle,alpha=0.0,gid='observation-full-lf')
ax_forecast.plot(x_forecast, y_forecast_lower, color=np.array(lower_color_limit)/256., alpha=0.0, zorder=2, gid = "LOWER-FORECAST-LINE")
ax_forecast.plot(x_forecast, y_forecast_median, color="k", alpha=0.0, zorder=2, gid = "MEDIAN-FORECAST-LINE")
ax_forecast.plot(x_forecast, y_forecast_upper, color=np.array(upper_color_limit)/256., alpha=0.0, zorder=2, gid = "UPPER-FORECAST-LINE")

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
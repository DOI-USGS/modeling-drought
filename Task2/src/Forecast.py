import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime
from scipy import interpolate
import re

mpl.rcParams["font.family"] = "monospace"
mpl.rcParams['svg.fonttype'] = 'none'

# user parameters
number_of_frames = 501
min_percentile = 0.05
prediction = -1  # -1 is the final prediction
date_range = ['1988-01-01','1992-01-01']
river_label = 'Colorado River Near Colorado-Utah State Line - 09163500'

# asymmetric laplace distribution parameters
# https://en.wikipedia.org/wiki/Asymmetric_Laplace_distribution
loc = 0.0
scale = 1.0
kappa = 0.5

# functions

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


forecast_files = ['ForJeffrey_0Week_forecasts.npz',
                  'ForJeffrey_1Week_forecasts.npz',
                  'ForJeffrey_2Week_forecasts.npz',
                  'ForJeffrey_4Week_forecasts.npz',
                  'ForJeffrey_9Week_forecasts.npz',
                  'ForJeffrey_13Week_forecasts.npz']

#colors = plt.cm.viridis(np.linspace(0,1,len(forecast_files)))
# load data
forecast_data = [np.load("Task_Data/" + forecast_file) for forecast_file in forecast_files]
x_forecast = forecast_data[0]["training_set_issue_dates"]
y_training = forecast_data[0]["training_set_targets"][0, :, 0] * 100.0
offset = [0,1,2,4,9,13]

y_forecast_lower = forecast_format(forecast_data[0]["iterative_training_set_predictions"][prediction, :, 0])
y_forecast_median = forecast_format(forecast_data[0]["iterative_training_set_predictions"][prediction, :, 1])
y_forecast_upper = forecast_format(forecast_data[0]["iterative_training_set_predictions"][prediction, :, 2])


# make figure
fig = plt.figure(0, figsize=(8, 4))
# add axes
ax_forecast = fig.add_axes([0.1, 0.175, 0.85, 0.75])

for j in range(310,520):
    x_cloud = x_forecast[j] + np.array(offset) * 7
    y_cloud_lower = []
    y_cloud_median = []
    y_cloud_upper = []

    for i, forecast_datum in enumerate(forecast_data):
        y_cloud_lower += [forecast_format(forecast_datum["iterative_training_set_predictions"][prediction, :, 0])[j+offset[i]]]
        y_cloud_median += [forecast_format(forecast_datum["iterative_training_set_predictions"][prediction, :, 1])[j+offset[i]]]
        y_cloud_upper += [forecast_format(forecast_datum["iterative_training_set_predictions"][prediction, :, 2])[j+offset[i]]]
       
    #plotting
    #predictions
    ax_forecast.plot(x_forecast[:1+j], y_forecast_lower[:1+j], color="tab:blue",alpha=0.0,gid='prediction_lower_'+str(j))
    ax_forecast.plot(x_forecast[:1+j], y_forecast_median[:1+j], color="k",alpha=0.0,gid='prediction_middl_'+str(j))
    ax_forecast.plot(x_forecast[:1+j], y_forecast_upper[:1+j], color="tab:orange",alpha=0.0,gid='prediction_upper_'+str(j))
    ax_forecast.fill_between(x_forecast[:1+j], y_forecast_lower[:1+j],y_forecast_upper[:1+j],color="tab:gray",alpha=0.0,edgecolor='none',gid='prediction_patch_'+str(j))
    
    #observation
    ax_forecast.plot(x_forecast[:1+j], y_training[:1+j], color="tab:red",alpha=0.0,gid='observation_'+str(j))
    
    #hover_line
    ax_forecast.plot([x_forecast[j],x_forecast[j]],[0,100], color="k",alpha=0.0,gid='forecast_hover_'+str(j),linewidth=2.5,zorder=100)

    # add forecast lines
    ax_forecast.plot(x_cloud , y_cloud_lower, color="tab:blue", linestyle="--",alpha=0.0,gid='forecast_lower_'+str(j))
    ax_forecast.plot(x_cloud , y_cloud_median,color='k',linestyle="--",alpha=0.0,gid='forecast_middl_'+str(j))
    ax_forecast.plot(x_cloud , y_cloud_upper, color="tab:orange", linestyle="--",alpha=0.0,gid='forecast_upper_'+str(j))
    # #fill between upper and lower
    ax_forecast.fill_between(x_cloud,y_cloud_lower,y_cloud_upper,color="tab:gray",alpha=0.0,edgecolor='none',gid='forecast_patch_'+str(j))

def selectable_text(ax,x,y,label,color,va,ha,gid):
    ax.text(x,y,label,color=color,va=va,ha=ha,gid=gid,transform=ax_forecast.transAxes,
    bbox=dict(facecolor="w", alpha=0.0000001, edgecolor="none", pad=0.0),zorder=1)

# add textbox for lines. Need a fix, when alpha is zero, the box is not rendered in the svg. Bandaid is to make alpha very very small.
selectable_text(ax_forecast,1.0,1.0, "Toggle Observations","tab:red","bottom","right","toggle-observations")

# forecast axis parameters
ax_forecast.plot(x_forecast, y_training, color="tab:red",alpha=0.0,gid='observation_full')
ax_forecast.grid(visible=True, axis="y")
ax_forecast.tick_params(direction="out")
ax_forecast.set_ylim(0, 100.0)
ax_forecast.set_xlim(np.datetime64(date_range[0]),np.datetime64(date_range[-1]))
start_year = 1970 + np.datetime64(date_range[0],'Y').astype(int)
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
fig.savefig("Task2/out/forecast.svg", dpi=150)

#remove metadata
remove_metadata("Task2/out/forecast.svg", "src/assets/svgs/forecast.svg")
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

# user parameters
number_of_frames = 501
min_percentile = 0.05
prediction =  -1 # -1 is the final prediction
date_range = ['2017-07-03','2019-07-01']
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


forecast_files = ['ForJeffrey_0day_forecast.feather',
                  'ForJeffrey_7day_forecast.feather',
                  'ForJeffrey_14day_forecast.feather',
                  'ForJeffrey_28day_forecast.feather',
                  'ForJeffrey_56day_forecast.feather',
                  'ForJeffrey_91day_forecast.feather']

#colors = plt.cm.viridis(np.linspace(0,1,len(forecast_files)))
offset = [0,1,2,4,8,13]
dt = 7
dense_dt = 1
# load data
forecast_data = [feather.read_feather("Task_Data/" + forecast_file) for forecast_file in forecast_files]
x_forecast_raw = forecast_data[0]["datetime"].values.astype('datetime64[D]')
y_training_raw = forecast_data[0]["observed"]
y_forecast_lower_raw = forecast_format(forecast_data[0]["lower"]/100.)
y_forecast_median_raw = forecast_format(forecast_data[0]["median"]/100.)
y_forecast_upper_raw = forecast_format(forecast_data[0]["upper"]/100.)

x_forecast = np.arange(x_forecast_raw[0],x_forecast_raw[-1],dense_dt)
dx_forecast_raw = x_forecast_raw - x_forecast_raw[0]
dx_forecast = x_forecast - x_forecast[0]
y_training = interpolate.interp1d(dx_forecast_raw.astype(float),y_training_raw)(dx_forecast.astype(float))
y_forecast_lower = interpolate.interp1d(dx_forecast_raw.astype(float),y_forecast_lower_raw)(dx_forecast.astype(float))
y_forecast_median = interpolate.interp1d(dx_forecast_raw.astype(float),y_forecast_median_raw)(dx_forecast.astype(float))
y_forecast_upper = interpolate.interp1d(dx_forecast_raw.astype(float),y_forecast_upper_raw)(dx_forecast.astype(float))

f_cloud_lower_list = []
f_cloud_median_list = []
f_cloud_upper_list = []
for i,forecast_datum in enumerate(forecast_data):
    x_forecast_raw_temp = forecast_data[i]["datetime"].values.astype('datetime64[D]')
    dx_forecast_raw_temp = x_forecast_raw_temp - x_forecast_raw_temp[0]
    f_cloud_lower_list += [interpolate.interp1d(dx_forecast_raw_temp.astype(float),forecast_format(forecast_datum["lower"]/100.))]
    f_cloud_median_list += [interpolate.interp1d(dx_forecast_raw_temp.astype(float),forecast_format(forecast_datum["median"]/100.))]
    f_cloud_upper_list += [interpolate.interp1d(dx_forecast_raw_temp.astype(float),forecast_format(forecast_datum["upper"]/100.))]

# make figure
fig = plt.figure(1, figsize=(8, 4),gid='figure-forecast')
# add axes
ax_forecast = fig.add_axes([0.1, 0.175, 0.85, 0.75],gid='axis-forecast')

print ('default ' + str(np.argmin(np.abs(x_forecast-np.datetime64(date_range[0])))))
ax_forecast.annotate('Drag mouse over the\nplot rightwards to see\ndought forecasts.', va = 'center',xy=(np.datetime64('2018-01-08'), 71), xytext=(np.datetime64('2017-07-08'), 71),arrowprops=dict(facecolor='black',arrowstyle='fancy', gid='annotation_forecast_arrow'),gid='annotation_forecast',fontweight='bold')
for j in range(np.argmin(np.abs(x_forecast-np.datetime64(date_range[0]))),np.argmin(np.abs(x_forecast-np.datetime64(date_range[1])))+1,int(dt/dense_dt)):
    x_cloud = x_forecast[j] + np.array(offset) * 7
    y_cloud_lower = []
    y_cloud_median = []
    y_cloud_upper = []

    for i in range(0,len(f_cloud_median_list)):
        lead_time = dx_forecast.astype(float)[j+int(offset[i]*dt/dense_dt)]
        y_cloud_lower += [f_cloud_lower_list[i](lead_time)]
        y_cloud_median += [f_cloud_median_list[i](lead_time)]
        y_cloud_upper += [f_cloud_upper_list[i](lead_time)]
       
    #plotting
    #predictions
    # ax_forecast.plot(x_forecast[:1+j], y_forecast_lower[:1+j], color="tab:blue",alpha=0.0,gid='prediction_lower_'+str(j))
    # ax_forecast.plot(x_forecast[:1+j], y_forecast_median[:1+j], color="k",alpha=0.0,gid='prediction_middl_'+str(j))
    # ax_forecast.plot(x_forecast[:1+j], y_forecast_upper[:1+j], color="tab:orange",alpha=0.0,gid='prediction_upper_'+str(j))
    # ax_forecast.fill_between(x_forecast[:1+j], y_forecast_lower[:1+j],y_forecast_upper[:1+j],color="tab:gray",alpha=0.0,edgecolor='none',gid='prediction_patch_'+str(j))
    
    #observation
    ax_forecast.plot(x_forecast[:1+j], y_training[:1+j], color="tab:red",alpha=0.0,gid='observation_'+str(j))
    
    #hover_line
    ax_forecast.plot([x_forecast[j],x_forecast[j]],[0,100], color="k",alpha=0.0,gid='forecast_hover_'+str(j),linewidth=5.,zorder=100)

    # # add forecast lines
    #ax_forecast.plot(x_cloud , y_cloud_lower, color="tab:blue", linestyle="--",alpha=0.0,gid='forecast_lower_'+str(j))
    ax_forecast.plot(x_cloud , y_cloud_median,color='k',linestyle="-",alpha=0.0,gid='forecast_middl_'+str(j), solid_capstyle='round')
    #ax_forecast.plot(x_cloud , y_cloud_upper, color="tab:orange", linestyle="--",alpha=0.0,gid='forecast_upper_'+str(j))
    # #fill between upper and lower
    # ax_forecast.fill_between(x_cloud,y_cloud_lower,y_cloud_upper,color="tab:gray",alpha=0.0,edgecolor='none',gid='forecast_patch_'+str(j))

    # # #fill between prediction and observation
    # ax_forecast.fill_between(x_forecast[:1+j], y_training[:1+j],y_forecast_median[:1+j],where=y_training[:1+j]>=y_forecast_median[:1+j],alpha=0.0,edgecolor='none',gid='overprediction_patch_'+str(j))
    # ax_forecast.fill_between(x_forecast[:1+j], y_training[:1+j],y_forecast_median[:1+j],where=y_training[:1+j]<=y_forecast_median[:1+j],alpha=0.0,edgecolor='none',gid='underprediction_patch_'+str(j))

def selectable_text(ax,x,y,label,color,va,ha,gid):
    ax.text(x,y,label,color='w',va=va,ha=ha,gid=gid,transform=ax_forecast.transAxes,
        bbox=dict(facecolor=color,boxstyle='round', alpha=1, edgecolor="k",pad=0.10,linewidth=0.75),zorder=1)
    shadow_color = (0.4,0.4,0.4)
    shadow_offset_x = 0.004
    shadow_offset_y = -0.005
    text = ax.text(x+shadow_offset_x,y+shadow_offset_y,label,color=shadow_color,va=va,ha=ha,gid='shadow-'+gid,transform=ax_forecast.transAxes,
        bbox=dict(facecolor=shadow_color,boxstyle='round', alpha=1, edgecolor=shadow_color,pad=0.10,linewidth=0.75),zorder=0)
    return (text.get_window_extent().transformed(plt.gca().transData.inverted()))

# add textbox for lines. Need a fix, when alpha is zero, the box is not rendered in the svg. Bandaid is to make alpha very very small.
bbox = selectable_text(ax_forecast,0.99,1.02, "Toggle Observations","tab:red","bottom","right","toggle-observations-forecast")
ax_forecast.annotate('Click button',fontweight='bold', va = 'bottom',ha='right',xy=(bbox.x0,0.5*(bbox.y0+bbox.y1)), xytext=(0.75,1.02),xycoords='axes fraction',gid='annotation_buttons3',arrowprops=dict(facecolor='black', shrinkB=5,gid='annotation_buttons3_arrow1',arrowstyle='->',connectionstyle='arc3,rad=0.0',alpha=0.8),zorder=10)

# forecast axis parameters
ax_forecast.plot(x_forecast, y_training, color="tab:red",alpha=0.0,gid='observation-full-forecast')
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
fig.savefig("Task2/out/fc_example.svg", dpi=150)

#remove metadata
remove_metadata("Task2/out/fc_example.svg", "src/assets/svgs/fc_example.svg")
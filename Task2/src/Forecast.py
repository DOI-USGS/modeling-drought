import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime
from scipy import interpolate
import re

mpl.rcParams["font.family"] = "monospace"

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

# make figure
fig = plt.figure(1, figsize=(10, 4))
# add axes
ax_forecast = fig.add_axes([0.1, 0.1, 0.85, 0.85])

forecast_files = ['ForJeffrey_0Week_forecasts.npz',
                  'ForJeffrey_1Week_forecasts.npz',
                  'ForJeffrey_2Week_forecasts.npz',
                  'ForJeffrey_4Week_forecasts.npz',
                  'ForJeffrey_9Week_forecasts.npz',
                  'ForJeffrey_13Week_forecasts.npz']
for forecast_file in forecast_files:
    # load data
    forecast_data = np.load("../in/" + forecast_file)
    
    #add offset
    offset = int(str(forecast_data["forecast_horizon"])[:-6])
    

    #dates
    data_len = len(forecast_data["training_set_issue_dates"])
    x_forecast = forecast_data["training_set_issue_dates"][offset:data_len]
    #observations
    y_training = forecast_data["training_set_targets"][0, 0:data_len-offset, 0] * 100.0
    # model data
    y_forecast_lower = forecast_format(forecast_data["iterative_training_set_predictions"][prediction, offset:data_len, 0])
    y_forecast_median = forecast_format(forecast_data["iterative_training_set_predictions"][prediction, offset:data_len, 1])
    y_forecast_upper = forecast_format(forecast_data["iterative_training_set_predictions"][prediction, offset:data_len, 2])
    
    #plotting
    #observations 
    ax_forecast.plot(x_forecast, y_training, color="tab:red",alpha=1.0)

    # add static forecast lines
    ax_forecast.plot(x_forecast, y_forecast_lower, color="tab:blue", linestyle="--",alpha=0.25)
    ax_forecast.plot(x_forecast, y_forecast_median, color="k", linestyle="--",alpha=0.25)
    ax_forecast.plot(x_forecast, y_forecast_upper, color="tab:orange", linestyle="--",alpha=0.25)
    # #fill between upper and lower
    # ax_forecast.fill_between(x_forecast,y_forecast_lower,y_forecast_upper,color="tab:gray",alpha=0.3,edgecolor='none')

# forecast axis parameters
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
fig.savefig("../out/forecast.png", dpi=150)
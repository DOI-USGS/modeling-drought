### Import Libraries
import numpy as np
from scipy import stats
import pyarrow.feather as feather

### Shared
min_percentile = 0.05
date_range = ["2017-07-03", "2019-07-01"]
river_label = ""  #'Colorado River Near Colorado-Utah State Line - 09163500'
labels_bump = 1.01  # label x location
button_padding = 0.2
obs_linestyle = "dotted"
# forecast data for task 1
forecast_data = feather.read_feather("Task_Data/ForJeffrey_7day_forecast.feather")
# Shadows parameters for buttons
shadow_color = (0.4, 0.4, 0.4)
shadow_offset_x = 0.004
shadow_offset_y = -0.005

# asymmetric laplace distribution parameters: https://en.wikipedia.org/wiki/Asymmetric_Laplace_distribution
loc = 0.0
scale = 1.0
kappa = 0.5

# find lower, upper and median of ALD
z_val_min = stats.laplace_asymmetric.ppf(
    min_percentile, kappa=kappa, loc=loc, scale=scale
)
z_val_max = stats.laplace_asymmetric.ppf(
    1.0 - min_percentile, kappa=kappa, loc=loc, scale=scale
)
if kappa < 1.0:
    z_median = loc - 1.0 / (kappa * scale) * np.log((1.0 + kappa**2.0) / (2.0))
else:
    z_median = loc + kappa / scale * np.log((1.0 + kappa**2.0) / (2.0 * kappa**2.0))

### Loss Function
basename_gid_lf = "lossfunction"
number_of_frames_lf = 501
static_alpha = 0.25
fill_alpha = 0.15
annotation_label_loc_lf = (0.65, 0.7)

### Prediction Interval
basename_gid_pi = "predictioninterval"
va_list = ["top", "center", "bottom"]
annotation_label_loc_pi = (0.75, 0.9)
missed_marker_size = 8.0

### Forecast
basename_gid_forecast = "forecast"
basename_gid_forecast_summary_1 = "forecast_summary_1"
basename_gid_forecast_summary_2 = "forecast_summary_2"
offset = [0, 1, 2, 4, 8, 13]
dt = 7
dense_dt = 1

forecast_files = [
    "ForJeffrey_0day_forecast.feather",
    "ForJeffrey_7day_forecast.feather",
    "ForJeffrey_14day_forecast.feather",
    "ForJeffrey_28day_forecast.feather",
    "ForJeffrey_56day_forecast.feather",
    "ForJeffrey_91day_forecast.feather",
]

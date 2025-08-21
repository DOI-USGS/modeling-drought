### Import Libraries
import numpy as np
from scipy import stats
import pandas as pd
import pyarrow.feather as feather

### Shared Parameters########################################################################################
#############################################################################################################

min_percentile = 0.05
date_range = ["2000-10-09", " 2002-09-16"]
year_label_offset = 20
label_year = "-11-01"
obs_linestyle = "dotted"
site_id = "13055000"

### LossFunction.py and PredictionInterval.py ###############################################################
#############################################################################################################

# forecast data
forecast_data_all = feather.read_feather(
    "Task_Data/all_horizon_LSTM_30_forecasts.feather"
)
forecast_data_site = forecast_data_all[forecast_data_all["site_id"] == site_id]
forecast_data = forecast_data_site[forecast_data_site["nday_forecast"] == 7.0]

# asymmetric laplace distribution parameters: https://en.wikipedia.org/wiki/Asymmetric_Laplace_distribution
loc = 0.0
scale = 1.0
kappa = 0.5

# find lower, upper, and median of asymmetric laplace distribution
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

# loss function, x
x_LF = np.array([-1.0, 0.0, 1.0])

### LossFunction.py #########################################################################################
#############################################################################################################

basename_gid_lf = "lossfunction"
number_of_frames_lf = 501
static_alpha = 0.25
fill_alpha = 0.15
annotation_label_loc_lf = (0.65, 0.7)

### PredictionInterval.py####################################################################################
#############################################################################################################

basename_gid_pi = "predictioninterval"
va_list = ["top", "center", "bottom"]
annotation_label_loc_pi = (0.75, 0.9)
missed_marker_size = 8.0

### Forecast.py##############################################################################################
#############################################################################################################

basename_gid_forecast = "forecast"
basename_gid_forecast_summary_1 = "forecast_summary_1"
basename_gid_true_false = "forecast_truefalse"
basename_gid_true_false_key = "forecast_truefalse_key"
basename_gid_true_false_summary = "forecast_truefalse_summary"
offset = [1, 2, 4, 8, 13]
dt = 7
dense_dt = 1

# forecast files
forecast_data_list = [
    forecast_data_site[forecast_data_site["nday_forecast"] == 7.0],
    forecast_data_site[forecast_data_site["nday_forecast"] == 14.0],
    forecast_data_site[forecast_data_site["nday_forecast"] == 28.0],
    forecast_data_site[forecast_data_site["nday_forecast"] == 63.0],
    forecast_data_site[forecast_data_site["nday_forecast"] == 91.0],
]

### Observation.py##############################################################################################
#############################################################################################################

# Shorten x-axis in mobile site
x_shorten_mobile = 0.575
x_label_section_mobile = x_shorten_mobile + 0.075


### ForecastDiagram.py#######################################################################################
#############################################################################################################

# real data for diagram
forecast_data_diagram = feather.read_feather(
    "Task_Data/ForJeffrey_0day_forecast.feather"
)

# starting index in the forecast data used to generate the diagram
index_plot = 158

### ForecastSummary.py ######################################################################################
#############################################################################################################

# this is the median observed prediction for the entire data set, calculated from the model results
median_obs = 49.0733279613215

# line width
line_width_summary = 5.0

# data used for the forecast summary
drought_data = pd.read_csv(
    "Task_Data/UQ_summaries_for_JeffreyHayley_4PanelClassificationTypesForDroughtOnly_20250527_interpolated.csv"
)


### All ForecastTrueFalseXXXXX.py ###########################################################################
#############################################################################################################

# data used for forecast summary
tf_d = pd.read_csv(
    "Task_Data/UQ_summaries_for_JeffreyHayley_4PanelClassificationTypesForDroughtOnly_DataCounts_20250812_interpolated.csv"
)

# labeling
text_bump = 0.5
label_pad = 0.1

### ForecastTrueFalseKey.py #################################################################################
#############################################################################################################

pad = 5.0
width = 1.0

row0 = 0.0
row1 = 10.0
row2 = 20.0

bar_alpha = 0.25
swoop_alpha = 0.05
label_alpha = 0.0

import os
import yaml

# Make output folders if they do not exist
if not os.path.exists("Task1/out"):
    os.makedirs("Task1/out")
if not os.path.exists("Task2/out"):
    os.makedirs("Task2/out")

# Read in Parameters from YAML
with open("Task_config/parameters.yaml", "r") as file:
    params = yaml.safe_load(file)

aspect = params["aspect"]
grays = params["grays"]
colors = params["colors"]
dates = params["dates"]
fontsize = params["fontsize"]
sankey_params = params["sankey"]

# Use rule all to define all outputs required
rule all:
    input:
        "src/assets/svgs/fc_art_desktop.svg",
        "src/assets/svgs/fc_diagram.svg",
        "src/assets/svgs/ob_example_mobile.svg",
        "src/assets/svgs/fc_example_desktop.svg",
        "src/assets/svgs/fc_example_mobile.svg",
        "src/assets/svgs/fc_example_tablet.svg",
        "src/assets/svgs/fc_tf_key_desktop.svg",
        "src/assets/svgs/fc_tf_key_mobile.svg",
        "src/assets/svgs/fc_tf_key_tablet.svg",
        "src/assets/svgs/fc_tf_sum_desktop.svg",
        "src/assets/svgs/fc_tf_sum_rw_desktop.svg",
        "src/assets/svgs/fc_tf_sum_yd_desktop.svg",
        "src/assets/svgs/fc_tf_sum_nd_desktop.svg",
        "src/assets/svgs/fc_tf_sum_mobile.svg",
        "src/assets/svgs/fc_tf_sum_rw_mobile.svg",
        "src/assets/svgs/fc_tf_sum_yd_mobile.svg",
        "src/assets/svgs/fc_tf_sum_nd_mobile.svg",
        "src/assets/svgs/fc_tf_sum_tablet.svg",
        "src/assets/svgs/fc_tf_sum_rw_tablet.svg",
        "src/assets/svgs/fc_tf_sum_yd_tablet.svg",
        "src/assets/svgs/fc_tf_sum_nd_tablet.svg",
        "src/assets/svgs/lf_diagram_desktop.svg",
        "src/assets/svgs/lf_diagram_mobile.svg",
        "src/assets/svgs/lf_diagram_tablet.svg",
        "src/assets/svgs/lf_example_desktop.svg",
        "src/assets/svgs/lf_example_mobile.svg",
        "src/assets/svgs/lf_example_tablet.svg",
        "src/assets/svgs/pi_example_desktop.svg",
        "src/assets/svgs/pi_example_mobile.svg",
        "src/assets/svgs/pi_example_tablet.svg"

# Generate the Loss Function Explorer Viz for desktop, mobile, and tablet
rule loss_function:
    params:
        aspect_double_plot_desktop = aspect["aspect_double_plot_desktop"],
        aspect_double_plot_tablet = aspect["aspect_double_plot_tablet"],
        aspect_double_plot_mobile = aspect["aspect_double_plot_mobile"],
        ratio_7 = grays["ratio_7"],
        lower_color_limit_hex = colors["lower_color_limit_hex"],
        median_color_hex = colors["median_color_hex"],
        upper_color_limit_hex = colors["upper_color_limit_hex"],
        observation_color_hex = colors["observation_color_hex"],
        site_id = params["site_id"],
        basename_gid_lf = params["gids"]["basename_gid_lf"],
        date_range = [dates["date_start"], dates["date_end"]],
        label_year = dates["label_year"],
        year_label_offset = dates["year_label_offset"],
        min_percentile = params["min_percentile"],
        number_of_frames_lf = params["lf"]["number_of_frames_lf"],
        static_alpha = params["lf"]["static_alpha"],
        fill_alpha = params["lf"]["fill_alpha"],
        loc = params["laplace"]["loc"],
        scale = params["laplace"]["scale"],
        kappa = params["laplace"]["kappa"]
    input:
        "Task_Data/all_horizon_LSTM_30_forecasts_20250916.feather"
    output:
        "src/assets/svgs/lf_example_desktop.svg",
        "src/assets/svgs/lf_example_mobile.svg",
        "src/assets/svgs/lf_example_tablet.svg"
    script:
        'Task1/src/LossFunction.py'

# Generate the Loss Function Diagram Viz for desktop, mobile, and tablet
rule loss_function_diagram:
    params:
        aspect_double_plot_desktop = aspect["aspect_double_plot_desktop"],
        aspect_double_plot_tablet = aspect["aspect_double_plot_tablet"],
        aspect_double_plot_mobile = aspect["aspect_double_plot_mobile"],
        min_percentile = params["min_percentile"],
        loc = params["laplace"]["loc"],
        scale = params["laplace"]["scale"],
        kappa = params["laplace"]["kappa"],
        lower_color_limit_hex = colors["lower_color_limit_hex"],
        median_color_hex = colors["median_color_hex"],
        upper_color_limit_hex = colors["upper_color_limit_hex"],
        static_alpha = params["lf"]["static_alpha"],
        fill_alpha = params["lf"]["fill_alpha"]
    output:
        "src/assets/svgs/lf_diagram_desktop.svg",
        "src/assets/svgs/lf_diagram_mobile.svg",
        "src/assets/svgs/lf_diagram_tablet.svg"
    script:
        'Task1/src/LossFunctionDiagram.py'

# Generate the Prediction Interval Explorer Viz for desktop, mobile, and tablet 
rule prediction_interval:
    params:
        aspect_double_plot_desktop = aspect["aspect_double_plot_desktop"],
        aspect_double_plot_tablet = aspect["aspect_double_plot_tablet"],
        aspect_double_plot_mobile = aspect["aspect_double_plot_mobile"],
        ratio_7 = grays["ratio_7"],
        lower_color_limit_hex = colors["lower_color_limit_hex"],
        median_color_hex = colors["median_color_hex"],
        upper_color_limit_hex = colors["upper_color_limit_hex"],
        observation_color_hex = colors["observation_color_hex"],
        site_id = params["site_id"],
        basename_gid_pi = params["gids"]["basename_gid_pi"],
        date_range = [dates["date_start"], dates["date_end"]],
        label_year = dates["label_year"],
        year_label_offset = dates["year_label_offset"],
        min_percentile = params["min_percentile"],
        number_of_frames_lf = params["lf"]["number_of_frames_lf"],
        static_alpha = params["lf"]["static_alpha"],
        fill_alpha = params["lf"]["fill_alpha"],
        loc = params["laplace"]["loc"],
        scale = params["laplace"]["scale"],
        kappa = params["laplace"]["kappa"],
        missed_marker_size = params["pi"]["missed_marker_size"]
    input:
        "Task_Data/all_horizon_LSTM_30_forecasts_20250916.feather"
    output:
        "src/assets/svgs/pi_example_desktop.svg",
        "src/assets/svgs/pi_example_mobile.svg",
        "src/assets/svgs/pi_example_tablet.svg"
    script:
        'Task1/src/PredictionInterval.py'

# Generate the Forecast Diagram, one version for all platforms
rule forecast_diagram:
    params:
        aspect_single_plot = aspect["aspect_single_plot"],
        index_plot = params["fd"]["index_plot"],
        median_color_hex = colors["median_color_hex"],
    input:
        "Task_Data/ForJeffrey_0day_forecast.feather"
    output:
        "src/assets/svgs/fc_diagram.svg"
    script:
        'Task2/src/ForecastDiagram.py'

# Generate the Forecast Explorer Viz for desktop, mobile, and tablet
# This also generates the Observation Explorer Viz for desktop and tablet
rule forecast:
    params:
        aspect_double_plot_desktop = aspect["aspect_double_plot_desktop"],
        aspect_double_plot_tablet = aspect["aspect_double_plot_tablet"],
        aspect_double_plot_mobile = aspect["aspect_double_plot_mobile"],
        target_fontsize_px = fontsize["target_fontsize_px"],
        ratio_7 = grays["ratio_7"],
        median_color_hex = colors["median_color_hex"],
        observation_color_hex = colors["observation_color_hex"],
        site_id = params["site_id"],
        basename_gid_forecast = params["gids"]["basename_gid_forecast"],
        date_range = [dates["date_start"], dates["date_end"]],
        label_year = dates["label_year"],
        year_label_offset = dates["year_label_offset"],
    input:
        "Task_Data/all_horizon_LSTM_30_forecasts_20250916.feather"
    output:
        "src/assets/svgs/fc_example_desktop.svg",
        "src/assets/svgs/fc_example_mobile.svg",
        "src/assets/svgs/fc_example_tablet.svg"
    script:
        'Task2/src/Forecast.py'

# Generate the Forecast Art Header Viz, one version for all platforms
rule forecast_art:
    params:
        aspect_double_plot_desktop = aspect["aspect_double_plot_desktop"],
        aspect_double_plot_tablet = aspect["aspect_double_plot_tablet"],
        aspect_double_plot_mobile = aspect["aspect_double_plot_mobile"],
        target_fontsize_px = fontsize["target_fontsize_px"],
        ratio_7 = grays["ratio_7"],
        median_color_hex = colors["median_color_hex"],
        observation_color_hex = colors["observation_color_hex"],
        site_id = params["site_id"],
        basename_gid_forecast = params["gids"]["basename_gid_forecast"],
        date_range = [dates["date_start"], dates["date_end"]],
        label_year = dates["label_year"],
        year_label_offset = dates["year_label_offset"]
    input:
        "Task_Data/all_horizon_LSTM_30_forecasts_20250916.feather"
    output:
        "src/assets/svgs/fc_art_desktop.svg"
    script:
        'Task2/src/ForecastArt.py'

# Generate the Observation Explorer Viz for mobile
rule observation:
    params:
        aspect_double_plot_desktop = aspect["aspect_double_plot_desktop"],
        aspect_double_plot_tablet = aspect["aspect_double_plot_tablet"],
        aspect_double_plot_mobile = aspect["aspect_double_plot_mobile"],
        target_fontsize_px = fontsize["target_fontsize_px"],
        ratio_7 = grays["ratio_7"],
        median_color_hex = colors["median_color_hex"],
        observation_color_hex = colors["observation_color_hex"],
        site_id = params["site_id"],
        basename_gid_forecast = params["gids"]["basename_gid_forecast"],
        date_range = [dates["date_start"], dates["date_end"]],
        label_year = dates["label_year"],
        year_label_offset = dates["year_label_offset"]
    input:
        "Task_Data/all_horizon_LSTM_30_forecasts.feather"
    output:
        "src/assets/svgs/ob_example_mobile.svg"
    script:
        'Task2/src/Observation.py'

# Generate the Sankey Viz for desktop, mobile, and tablet
rule truefalsekey:
    params:
        aspect_single_plot = aspect["aspect_single_plot"],
        basename_gid_true_false_key = params["gids"]["basename_gid_true_false_key"],
        pad = sankey_params["pad"],
        width = sankey_params["width"],
        row0 = sankey_params["row0"],
        row1 = sankey_params["row1"],
        row2 = sankey_params["row2"],
        bar_alpha = sankey_params["bar_alpha"],
        swoop_alpha = sankey_params["swoop_alpha"],
        label_alpha = sankey_params["label_alpha"],
        lower_color_limit_hex = colors["lower_color_limit_hex"],
        upper_color_limit_hex = colors["upper_color_limit_hex"],
        lower_color_limit_hex_half_alpha = colors["lower_color_limit_hex_half_alpha"],
        upper_color_limit_hex_half_alpha = colors["upper_color_limit_hex_half_alpha"]
    input:
        "Task_Data/UQ_summaries_for_JeffreyHayley_4PanelClassificationTypesForDroughtOnly_DataCounts_20250916.csv"
    output:
        "src/assets/svgs/fc_tf_key_desktop.svg",
        "src/assets/svgs/fc_tf_key_mobile.svg",
        "src/assets/svgs/fc_tf_key_tablet.svg"
    script:
        'Task2/src/ForecastTrueFalseKey.py'

# Generate the Sankey Summary for desktop, mobile, and tablet
rule truefalsesum:
    params:
        aspect_single_plot = aspect["aspect_single_plot"],
        basename_gid_true_false_summary = params["gids"]["basename_gid_true_false_summary"],
        lower_color_limit_hex = colors["lower_color_limit_hex"],
        upper_color_limit_hex = colors["upper_color_limit_hex"],
        lower_color_limit_hex_half_alpha = colors["lower_color_limit_hex_half_alpha"],
        upper_color_limit_hex_half_alpha = colors["upper_color_limit_hex_half_alpha"],
        ratio_7 = grays["ratio_7"],
        text_bump = params["sankey_sum"]["text_bump"],
        label_pad = params["sankey_sum"]["label_pad"]
    input:
        "Task_Data/UQ_summaries_for_JeffreyHayley_4PanelClassificationTypesForDroughtOnly_DataCounts_20250916.csv"
    output:
        "src/assets/svgs/fc_tf_sum_desktop.svg",
        "src/assets/svgs/fc_tf_sum_mobile.svg",
        "src/assets/svgs/fc_tf_sum_tablet.svg"
    script:
        'Task2/src/ForecastTrueFalseSummary.py'

# Generate the Sankey Outcome Plots for desktop, mobile, and tablet
rule truefalse_outcomes:
    params:
        aspect_single_plot = aspect["aspect_single_plot"],
        basename_gid_true_false_summary = params["gids"]["basename_gid_true_false_summary"],
        lower_color_limit_hex = colors["lower_color_limit_hex"],
        upper_color_limit_hex = colors["upper_color_limit_hex"],
        lower_color_limit_hex_half_alpha = colors["lower_color_limit_hex_half_alpha"],
        upper_color_limit_hex_half_alpha = colors["upper_color_limit_hex_half_alpha"],
        ratio_3 = grays["ratio_3"],
        ratio_7 = grays["ratio_7"],
        text_bump = params["sankey_sum"]["text_bump"],
        label_pad = params["sankey_sum"]["label_pad"]
    input:
        "Task_Data/UQ_summaries_for_JeffreyHayley_4PanelClassificationTypesForDroughtOnly_DataCounts_20250916.csv"
    output:
        "src/assets/svgs/fc_tf_sum_nd_desktop.svg",
        "src/assets/svgs/fc_tf_sum_yd_desktop.svg",
        "src/assets/svgs/fc_tf_sum_rw_desktop.svg",
        "src/assets/svgs/fc_tf_sum_nd_mobile.svg",
        "src/assets/svgs/fc_tf_sum_yd_mobile.svg",
        "src/assets/svgs/fc_tf_sum_rw_mobile.svg",
        "src/assets/svgs/fc_tf_sum_nd_tablet.svg",
        "src/assets/svgs/fc_tf_sum_yd_tablet.svg",
        "src/assets/svgs/fc_tf_sum_rw_tablet.svg"
    script:
        'Task2/src/ForecastTrueFalseOutcomes.py'
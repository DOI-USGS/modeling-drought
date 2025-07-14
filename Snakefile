rule all:
    input:
        "src/assets/svgs/lf_example_tablet.svg",
        "src/assets/svgs/pi_example_tablet.svg",
        "src/assets/svgs/fc_diagram.svg",
        "src/assets/svgs/fc_example_desktop.svg",
        "src/assets/svgs/fc_summary_desktop.svg",
        "src/assets/svgs/fc_tf_key_desktop.svg",
        "src/assets/svgs/fc_tf_sum_desktop.svg",
        "src/assets/svgs/fc_tf_sum_rw_desktop.svg",
        "src/assets/svgs/fc_tf_sum_yd_desktop.svg",
        "src/assets/svgs/fc_tf_sum_nd_desktop.svg",

rule loss_function:
    output:
        "src/assets/svgs/lf_example_tablet.svg"
    script:
        'Task1/src/LossFunction.py'

rule prediction_interval:
    output:
        "src/assets/svgs/pi_example_tablet.svg"
    script:
        'Task1/src/PredictionInterval.py'

rule forecast_diagram:
    output:
        "src/assets/svgs/fc_diagram.svg"
    script:
        'Task2/src/ForecastDiagram.py'

rule forecast:
    output:
        "src/assets/svgs/fc_example_desktop.svg"
    script:
        'Task2/src/Forecast.py'

rule summary:
    output:
        "src/assets/svgs/fc_summary_desktop.svg"
    script:
        'Task2/src/ForecastSummary.py'

rule truefalsekey:
    output:
        "src/assets/svgs/fc_tf_key_desktop.svg"
    script:
        'Task2/src/ForecastTrueFalseKey.py'

rule truefalsesum:
    output:
        "src/assets/svgs/fc_tf_sum_desktop.svg"
    script:
        'Task2/src/ForecastTrueFalseSummary.py'

rule truefalsesum_rw:
    output:
        "src/assets/svgs/fc_tf_sum_rw_desktop.svg"
    script:
        'Task2/src/ForecastTrueFalseSummary_rw.py'

rule truefalsesum_yd:
    output:
        "src/assets/svgs/fc_tf_sum_yd_desktop.svg"
    script:
        'Task2/src/ForecastTrueFalseSummary_yd.py'

rule truefalsesum_nd:
    output:
        "src/assets/svgs/fc_tf_sum_nd_desktop.svg"
    script:
        'Task2/src/ForecastTrueFalseSummary_nd.py'
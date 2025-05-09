import ForecastConfidence from "../../components/ForecastConfidence.vue";
import references from "./references";

export default {
    pageTitle: "Modeling <span class='emph'>streamflow</span> drought",
    sections: {
        A: {
            title: "How do we capture uncertainty?",
            subtitle:"We train the model to give us the range of possible streamflow percentiles.",
            paragraph1: "When we forecast streamflow, we want to know the uncertainty associated with each prediction.",
            paragraph2: "To capture the uncertainty, we train the model to predict three things: <ul>The model’s best estimate of the streamflow percentile (this is the median prediction.</ul><ul>The upper bound for the streamflow percentile (this is the 95% quantile). The model is predicting that 95% of future observed streamflow levels will be lower than this percentile.</ul><ul>The lower bound for the streamflow percentile (this is the 5% quantile). The model is predicting that 5% of future observed streamflow levels will be higher than this percentile.</ul>"
        },
        B: {
            title: "How confidence changes with lead time",
        },
        C: {
            title: "Event-driven metrics for model evaluation",
        },
        D: {
            title: "About the data-driven drought team",
        },
        references: {
            title: "References"
        },
        authors: {
            title: "USGS Vizlab"
        }
    },
    components: {
        LossFunction: {
            heading: "Loss Function",
            paragraph1: "When we train the machine learning model, we incentivize it to find the best solution by penalizing it when it predicts incorrectly. The further the model being correct, the more we penalize it. If we penalize the model the same for under- and overestimations, the model will try to best estimate the observation (a median prediction). We tell the model the equally penalize under- and overestimations by specifying a loss function that is symmetric",
            paragraph2: "The loss function determines how the model is penalized, the higher the line is, the more the model is penalized. Left of the median corresponds to underestimations, and right of the median corresponds to overestimations. We can change this loss function to change how the model is penalized for under- and overestimations. Hover your mouse over the loss function plot to see how it changes the model prediction below.",
            caption1Desktop: "Hover your mouse in the gray region to see the relationship between the loss function (left) and the stream flow percentile prediction (right).",
            caption1Responsive: "Tap in the gray region to see the relationship between the loss function (left) and the stream flow percentile prediction (right).",
            paragraph3: "What did you see? When the left slope in the loss function is gentler than the right slope, the model favors low predictions. The other way around, the model favors higher predictions. If we know which predictions are low and which are high, we can bracket the range of the model's predictions, where encompasses the majority of the observations. This range defines the model's uncertainity."
        },
        PredictionInterval: {
            heading: "Prediction Interval",
            paragraph1: "By setting more asymmetric loss functions, we can widen the prediction envelope, which we call a confidence interval. The percentage of the confidence interval tells us what percentage of the observations we expect to be within the interval.",
            caption: "Use the radio buttons to explore the loss functions (left) and corresponding confidence intervals (right).",
        },
        ForecastConfidence: {
            heading: "Forecast",
            paragraph1: "A paragraph.",
            caption1Desktop: "Hover your mouse over the plot to see how the model forecasts streamflow drought.",
            caption1Responsive: "Tap on the plot to see how the model forecasts streamflow drought.",
        },
        ForecastSummary: {
            heading: "Forecast Summary",
            paragraph1: "A paragraph.",
            caption1Desktop: "Hover your mouse over the plot to see ...TBA",
            caption1Responsive: "Tap the plot to see ...TBA",
        },
        AboutTheTeam: {
            heading: "Collaboration across the water community",
            paragraph1: "An interdisciplinary team of USGS researchers and data scientists are working together to forecast streamflow drought at a national scale.",
            paragraph2: "This is a collective effort by the <span class='group-label' data-group='OPP'>Office of Planning and Programming</span>, <span class='group-label' data-group='IMPD'>Integrated Modeling and Prediction Division</span>, <span class='group-label' data-group='OSD'>Observing Systems Division</span>,  <span class='group-label' data-group='IIDD'>Integrated Information Dissemination Division</span>, <span class='group-label' data-group='ESPD'>Earth Systems Processes Division</span>, <span class='group-label' data-group='OR'>OR Water Science Center</span>, <span class='group-label' data-group='MD-DE-DC'>MD-DE-DC Water Science Center</span>, <span class='group-label' data-group='WY-MT'>WY-MT Water Science Center</span> and <span class='group-label' data-group='UT'>UT Water Science Center</span>.",
        }
    }
}
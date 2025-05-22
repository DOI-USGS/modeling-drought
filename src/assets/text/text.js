import Forecaste from "../../components/Forecast.vue";
import references from "./references";

export default {
    pageTitle: "Modeling <span class='emph'>streamflow</span> drought",
    sections: {
        A: {
            title: "How uncertainty is quantified",
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
            heading: "How do we capture uncertainty? Part 1",
            paragraph1: "When we train the machine learning model, we incentivize it to find the best solution by penalizing it when it predicts incorrectly. The further the model being correct, the more we penalize it. If we penalize the model the same for under- and overestimations, the model will try to best estimate the observation (a median prediction). We tell the model the equally penalize under- and overestimations by specifying a loss function that is symmetric",
            paragraph2: "The loss function determines how the model is penalized, the higher the line is, the more the model is penalized. Left of the median corresponds to underestimations, and right of the median corresponds to overestimations. We can change this loss function to change how the model is penalized for under- and overestimations. Hover your mouse over the loss function plot to see how it changes the model prediction below.",
            caption1Desktop: "Hover your mouse in the gray region to see the relationship between the loss function (left) and the stream flow percentile prediction (right).",
            caption1Responsive: "Tap in the gray region to see the relationship between the loss function (left) and the stream flow percentile prediction (right).",
            paragraph3: "What did you see? When the left slope in the loss function is gentler than the right slope, the model favors low predictions. The other way around, the model favors higher predictions. If we know which predictions are low and which are high, we can bracket the range of the model's predictions, where encompasses the majority of the observations. This range defines the model's uncertainity."
        },
        PredictionInterval: {
            heading: "How do we capture uncertainty? Part 2",
            paragraph1: "By setting more asymmetric loss functions, we can widen the prediction envelope, which we call a confidence interval. The percentage of the confidence interval tells us what percentage of the observations we expect to be within the interval.",
            caption: "Use the radio buttons to explore the loss functions (left) and corresponding confidence intervals (right).",
        },
        Forecast: {
            heading: "What do the forecasts look like?",
            paragraph1: "We generate weekly forecasts for 1 - 13 weeks in the future",
            caption1Desktop: "Hover your mouse over the plot to see how the model forecasts streamflow drought.",
            caption1Responsive: "Tap on the plot to see how the model forecasts streamflow drought.",
        },
        ForecastSummary: {
            heading: "How does uncertainty change with forecast horizon?",
            paragraph1: "A paragraph.",
            caption1Desktop: "Hover your mouse over the plot to explore how the model's uncertainty changes with forecast horizon.",
            caption1Responsive: "Tap the plot to explore how the model's uncertainty changes with forecast horizon.",
        },
        ForecastTrueFalseSankey: {
            heading: "How well does the model perform? Part 1",
            paragraph1: "More droughts get missed further into the future",
            caption1Desktop: "Hover your mouse over the Sankey plot to see how often the model predicts drought or now, and how that prediction is correct (true outcome).",
            caption1Responsive: "Tap the Sankey plot to see how often the model predicts drought or now, and how that prediction is correct (true outcome).",
        },
        ForecastTrueFalseSummary: {
            heading: "How well does the model perform? Part 2",
            paragraph1: "For a given horizon...",
            caption: "Depending on the forecast horizon, the proportions of true-positives, true-negatives, false-positives, and false-negatives changes. More false outcomes occurs as forecast horizon increases.",
        },
        ForecastTrueFalseRightOrWrong: {
            heading: "How well does the model perform? Part 3",
            paragraph1: "For a given horizon...",
            caption: "Use the radio buttons to see how the overall model performance and how right or wrong the model is depending on whether it predicts drought or not. The model's prediction ability is better with shorter forecast horizons.",
        },
        AboutTheTeam: {
            heading: "Collaboration across the water community",
            paragraph1: "An interdisciplinary team of USGS researchers and data scientists are working together to forecast drought at a national-scale. This is a collective effort by the <span class='group-label' data-group='ESPD'>Earth Systems Processes Division</span>, <span class='group-label' data-group='IIDD'>Integrated Information Dissemination Division</span>, <span class='group-label' data-group='IMPD'>Integrated Modeling and Prediction Division</span>, <span class='group-label' data-group='OSD'>Observing Systems Division</span>, <span class='group-label' data-group='OPP'>Office of Planning and Programming</span>, <span class='group-label' data-group='MD-DE-DC'>MD-DE-DC Water Science Center</span>, <span class='group-label' data-group='OR'>OR Water Science Center</span>, <span class='group-label' data-group='UT'>UT Water Science Center</span> and <span class='group-label' data-group='WY-MT'>WY-MT Water Science Center</span>.",
            caption: " ",
        }
    }
}
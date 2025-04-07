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
            heading: "Loss Function",
            paragraph1: "When we train the machine learning model, we incentivize it to find the best solution by penalizing it when it predicts incorrectly. The further the model being correct, the more we penalize it. If we penalize the model the same for under- and overestimations, the model will try to best estimate the observation (a median prediction). We tell the model the equally penalize under- and overestimations by specifying a loss function that is symmetric",
            paragraph2: "The loss function determines how the model is penalized, the higher the line is, the more the model is penalized. Left of the median corresponds to underestimations, and right of the median corresponds to overestimations. We can change this loss function to change how the model is penalized for under- and overestimations. Hover your mouse over the loss function plot to see how it changes the model prediction below.",
            caption: "Hover your mouse in the gray region to see the relationship between the loss function (left) and the stream flow percentile prediciton (right).",
            paragraph3: "What did you see? When the left slope in the loss function is gentler than the right slope, the model favors low predictions. The other way around, the model favors higher predictions. If we know which predictions are low and which are high, we can bracket the range of the model's predictions, where encompasses the majority of the observations. This range defines the model's uncertainity."
        },
        PredictionInterval: {
            heading: "Prediction Interval",
            paragraph1: "By setting more asymmetric loss functions, we can widen the prediction envelope, which we call a confidence interval. The percentage of the confidence interval tells us what percentage of the observations we expect to be within the interval.",
            caption: "Use the radio buttons to explore the loss functions (left) and corresponding confidence intervals (right).",
        },
        Forecast: {
            heading: "Forecast",
            paragraph1: "",
            caption: "Hover your mouse over the plot to see the how the model forcasts drought.",
        },
        ForecastSummary: {
            heading: "Forecast Summary",
            paragraph1: "",
            caption: "Hover your mouse over the plot to see ...TBA",
        },
        AboutTheTeam: {
            heading: "USGS researchers and data scientists collaborate",
            paragraph1: "That's how science gets done. Here is a paragraph about the team. They're making it happen at USGS.",
            caption: "A caption could go here",
        }
    }
}
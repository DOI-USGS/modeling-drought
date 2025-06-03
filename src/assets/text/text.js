import ForecastConfidence from "../../components/ForecastConfidence.vue";
import WhatIsStreamflowDrought from "../../components/WhatIsStreamflowDrought.vue";
import references from "./references";

export default {
    pageTitle: "Modeling <span class='emph'>streamflow</span> drought",
    sections: {
        WhatIsStreamflowDrought: {
            title: "What is streamflow drought?",
            subtitle:"Streamflow droughts occur when streamflow levels become unusually low",
            paragraph1: "<a href='https://water.usgs.gov/vizlab/what-is-drought/' target='_blank'>Streamflow drought</a> occurs in the wake of meteorological and agricultural drought, when streamflow levels become unusually low. Reduced streamflow has significant impact on plants, animals, and humans.",
            accordionData: [
                {
                    heading: "Defining ‘unusually low’ streamflow using percentiles",
                    content: [
                        {
                            type: "text",
                            content: "For any stream or river, defining ‘unusually low’ streamflow means understanding typical conditions throughout the year. For <a href='https://labs.waterdata.usgs.gov/visualizations/gages-through-the-ages/index.html' target='_blank'>stream gages</a> with at least 40 years of data, we have a good understanding of what streamflow levels are typically observed at that site. "
                        },
                        {
                            type: "text",
                            content: "To categorize streamflow levels for each day of the year, we can use units of percentiles. If streamflow at a site on February 3<sup>rd</sup> is lower than 100 cubic feet per second (cfs) 50% of the time, then that streamflow level of 100 cfs is the 50<sup>th</sup> percentile, or median streamflow, at that site on February 3<sup>rd</sup>.  In contrast, a 20<sup>th</sup> percentile streamflow for that site on February 3<sup>rd</sup> is the level of streamflow that the site falls below on February 3<sup>rd</sup> in 20% of years. Another way to say it is that on February 3<sup>rd</sup>, streamflow at that site is less than that 20<sup>th</sup> percentile level 20% of the time."
                        },
                        {
                            type: "image",
                            content: "percentiles_explainer.png"
                        },
                        {
                            type: "text",
                            content: "For a given site, we define the 20<sup>th</sup> percentile streamflow on each day of the year as the threshold for drought for that day — any flow below this level is considered unusually low and is classified as a streamflow drought. "
                        }
                    ],
                    activeOnLoad: false
                },
                {
                    heading: "Classifying streamflow drought using percentiles",
                    content: [
                        {
                            type: "text",
                            content: "In addition to defining 20<sup>th</sup> percentile streamflow as the threshold for streamflow drought, we can use percentiles to further classify the category of drought: <span><ul><20<sup>th</sup> percentile = moderate drought</ul><ul>< 10<sup>th</sup> percentile = severe drought</ul><ul>< 5<sup>th</sup> percentile = extreme drought</ul></span>"
                        }
                    ],
                    activeOnLoad: false
                },
                {
                    heading: "How are ‘low flows’ different from ‘streamflow drought’?",
                    content: [
                        {
                            type: "text",
                            content: "It’s important to note the difference between ‘low streamflow’ and ‘streamflow drought.’ Low flows occur seasonally in many streams and are in line with typical conditions. In contrast, streamflow drought results when flows are unusually low compared to typical conditions."
                        },
                        {
                            type: "quote",
                            content: '"While droughts may include periods of low flows, a recurring seasonal low flow event is not necessarily a drought."—WMO, 2008'
                        }
                    ],
                    activeOnLoad: false
                }
            ]
        },
        HowModelStreamflowDrought: {
            title: "How do we model streamflow drought?",
            subtitle:"We train a model to accurately predict <i>low</i> streamflow percentiles",
            paragraph1: "To forecast streamflow drought across the contiguous United States (CONUS), we use a type of machine learning model called a Long Short-Term Memory (LSTM) network to predict streamflow percentiles.  To predict streamflow percentiles, we train the model with input data and output data for all for of CONUS for a specific historical time period: <span><ul>Input data: Static watershed characteristics (e.g., watershed area, land cover, topography, soil types), antecedent precipitation, temperature, snow water equivalent, soil moisture, weather and streamflow, and weather forecasts</ul><ul>Output data: Observed streamflow percentiles. Because streamflow droughts occur when streamflow is unusually low, we specifically train the model to predict low streamflow percentiles by restricting the training dataset to observed streamflow levels that fall below the 30th percentile</ul></span>",
            paragraph2: "Using cloud computing resources, the model is trained to “learn” the relationship between the input and output data.  With access to a broad training dataset with detailed information for so many watersheds, the model learns that the same weather can lead to different relative streamflow conditions (streamflow percentiles) at different sites.",
            paragraph3: "We use the final CONUS-wide model to predict streamflow percentiles for all future locations and dates. We convert the predicted percentiles to forecasts of streamflow drought by classifying the predicted percentile for each site based on the established drought thresholds (e.g., if the model predicts a 13th-percentile streamflow for a site, the model is predicting a moderate streamflow drought for that site)."
        },
        C: {
            title: "",
            subtitle:""
        },
        D: {
            title: "",
            subtitle:""
        },
        E: {
            title: "How do we capture uncertainty?",
            subtitle:"We train the model to give us the range of possible streamflow percentiles.",
            paragraph1: "When we forecast streamflow, we want to know the uncertainty associated with each prediction.",
            paragraph2: "To capture the uncertainty, we train the model to predict three things: <ul>The model’s best estimate of the streamflow percentile (this is the median prediction.</ul><ul>The upper bound for the streamflow percentile (this is the 95% quantile). The model is predicting that 95% of future observed streamflow levels will be lower than this percentile.</ul><ul>The lower bound for the streamflow percentile (this is the 5% quantile). The model is predicting that 5% of future observed streamflow levels will be higher than this percentile.</ul>"
        },
        F: {
            title: "How confidence changes with lead time",
        },
        G: {
            title: "What comes next?",
        },
        H: {
            title: "Who is contributing to this project?",
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
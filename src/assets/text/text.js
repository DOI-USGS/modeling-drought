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
                            content: "In addition to defining 20<sup>th</sup> percentile streamflow as the threshold for streamflow drought, we can use percentiles to further classify the category of drought: <span><ul>< 20<sup>th</sup> percentile = moderate drought</ul><ul>< 10<sup>th</sup> percentile = severe drought</ul><ul>< 5<sup>th</sup> percentile = extreme drought</ul></span>"
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
        WhatDoForecastsLookLike: {
            title: "What do the forecasts look like?",
            subtitle: "We generate weekly forecasts for 1-13 weeks in the future",
            forecastTimeseries: {
                paragraph1: "Every week, we ask the model to generate weekly forecasts for 1-13 weeks out. The model produces a prediction (its best estimate of the streamflow percentile for each week) along with a 90% prediction interval that captures the uncertainty of the prediction. More on that piece later!",
            },
            forecastExplore: {
                paragraph1: "We regenerate the forecast weekly – explore the figure below to see how the forecast updates over time, and how it compares to observations.",
                caption1Desktop: "Hover your mouse over the plot to see how the model forecasts streamflow drought.",
                caption1Responsive: "Tap on the plot to see how the model forecasts streamflow drought.",
            }
        },
        HowWellModelPerform: {
            title: "How well does the model perform?",
            subtitle: "More droughts get missed further into the future",
            forecastTrueFalseSankey: {
                paragraph1: "In order to evaluate how well the model performs, we can lump the predictions into four bins: <span><ul>True negatives: the model did not predict drought, and no drought occurred</ul><ul>False negatives: the model did not predict drought, but a drought occurred </ul><ul>True positives: the model predicted drought, and a drought occurred</ul><ul>False positives: the model predicted drought, but no drought occurred</ul></span>",
                paragraph2: "If we categorize all predictions that were generated for 1 week in the future, we see this:",
                caption1Desktop: "Hover your mouse over the Sankey plot to see how often the model predicts drought or not, and how often that prediction is correct (a ‘true’ outcome).",
                caption1Responsive: "Tap the Sankey plot to see how often the model predicts drought or not, and how often that prediction is correct (a ‘true’ outcome).",
                paragraph3: "Overall, the model does a good job of correctly predicting when streamflow drought will and will not occur 1 week in the future."
            },
            forecastTrueFalseSummary: {
                paragraph1: "As we generate forecasts for weeks that are further out, accuracy decreases:",
                caption: "Depending on the forecast horizon, the proportion of true positives, true negatives, false positives, and false negatives changes. More ‘false’ outcomes occur as the forecast horizon lengthens."
            },
            forecastTrueFalseRightOrWrong: {
                paragraph1: "Depending on what we’re interested in, we can look at just a subset of the results:",
                questionAll: "How often is the model right or wrong?",
                questionNoDrought: "If the model does not predict drought, how often is it right or wrong?",
                questionDrought: "If the model predicts drought, how often is it right or wrong?",
                caption: "Use the radio buttons to see how the overall model performance and how right or wrong the model is depending on whether it predicts drought or not. The model's prediction ability is better with shorter forecast horizons."
            }
        },
        HowCaptureUncertainty: {
            title: "How do we capture uncertainty?",
            subtitle:"We train the model to give us a range of possible values",
            paragraph1: "When we forecast streamflow percentiles, we want to know the uncertainty associated with each prediction. To capture the uncertainty, we train the model to predict three things:<span><ul>The model’s best estimate of the streamflow percentile for each forecast date—this is the median prediction</ul><ul>The upper bound for the streamflow percentile—this is the 95% quantile. The model is predicting that 95% of future observed streamflow levels on the forecast date will be lower than this percentile </ul><ul>The lower bound for the streamflow percentile—this is the 5% quantile. The model is predicting that 95% of future observed streamflow levels on the forecast date will be higher than this percentile</ul></span>",
            paragraph2: "Essentially, we want the model to consider everything that could happen, given the current inputs, and give us the range of possible streamflow percentiles, excluding the 10% least likely scenarios.",
            paragraph3: "We set up the model to generate these three predicted values by using what are called loss functions.",
            lossFunction: {
                heading: "Using loss functions",
                paragraph1: "When we train the machine learning model, we incentivize it to find the best solution by penalizing it when it predicts incorrectly. In general, the more inaccurate the prediction, the higher the penalty. But some of the incorrect predictions may be higher than the actual value (overestimates), while some may be lower than the actual value (underestimates). Depending on what we are asking the model to predict, we want to penalize it differently for over- and under- estimations.",
                paragraph2: "To set the model up to generate the median prediction, we use a loss function that penalizes the model equally for under- and over- estimations. When plotted, this loss function has identical left and right slopes, so we call this a symmetric loss function. Incorrect predictions are penalized more the further they are from the actual value, regardless of whether they are over- or under- estimations.",
                paragraph3: "To set the model up to generate the upper bound prediction, we use a loss function that penalizes the model more steeply for under- estimating the actual value than for over-estimating it. When plotted, this loss function has a steeper left slope than right slope, so we call this an asymmetric loss function.",
                paragraph4: "To set the model up to generate the lower bound prediction, we do the opposite, using a loss function that penalizes the model more steeply for over-estimating the actual value. When plotted, this loss function is also asymmetric, with a steeper right slope than left slope.",
                paragraph5: "Explore the plot below to see how the asymmetry of the loss function influences model predictions:",
                captionDesktop: "Hover your mouse in the gray region to see the relationship between the loss function (left) and the stream flow percentile prediction (right).",
                captionResponsive: "Tap in the gray region to see the relationship between the loss function (left) and the stream flow percentile prediction (right).",
                paragraph6: "What do you see? When the left slope in the loss function is steeper than the right slope, the model favors high predictions, as we would expect. And the other way around, the model favors low predictions. This approach allows the model to bracket the range of its predictions, capturing the uncertainty."
            },
            predictionInterval: {
                heading: "The prediction interval",
                paragraph1: "The upper and lower bounds that the model predicts define what we call the prediction interval. In this case, the model is predicting a 90% prediction interval. The percentage of the prediction interval tells us the approximate percentage of actual observations the model expects to be within the interval.",
                paragraph2: "You can see that the model does a good job of capturing the expected percent of observations if we specify different prediction intervals:",
                caption: "Use the radio buttons to explore the loss functions (left) and corresponding confidence intervals (right).",
                paragraph3: "Notice that the steeper the asymmetric loss functions, the wider the resulting prediction interval."
            }
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
        ForecastSummary: {
            heading: "How does uncertainty change with forecast horizon?",
            paragraph1: "A paragraph.",
            caption1Desktop: "Hover your mouse over the plot to explore how the model's uncertainty changes with forecast horizon.",
            caption1Responsive: "Tap the plot to explore how the model's uncertainty changes with forecast horizon.",
        },
        AboutTheTeam: {
            heading: "Collaboration across the water community",
            paragraph1: "An interdisciplinary team of USGS researchers and data scientists are working together to forecast streamflow drought at a national scale.",
            paragraph2: "This is a collective effort by the <span class='group-label' data-group='OPP'>Office of Planning and Programming</span>, <span class='group-label' data-group='IMPD'>Integrated Modeling and Prediction Division</span>, <span class='group-label' data-group='OSD'>Observing Systems Division</span>,  <span class='group-label' data-group='IIDD'>Integrated Information Dissemination Division</span>, <span class='group-label' data-group='ESPD'>Earth Systems Processes Division</span>, <span class='group-label' data-group='OR'>OR Water Science Center</span>, <span class='group-label' data-group='MD-DE-DC'>MD-DE-DC Water Science Center</span>, <span class='group-label' data-group='WY-MT'>WY-MT Water Science Center</span> and <span class='group-label' data-group='UT'>UT Water Science Center</span>.",
        }
    }
}
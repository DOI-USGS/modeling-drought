export default {
    pageTitle: "Modeling <span class='emph'>streamflow drought</span>",
    WhyForecastStreamflowDrought: {
        observationExplore: {
            caption1Desktop: "Hover your mouse over the plot to see when a stream goes into streamflow drought.",
            caption1Responsive: "Tap on the plot to see when a stream goes into streamflow drought.",
        },
        title: "Why forecast streamflow drought?",
        subtitle:"Streamflow drought forecasts help decision makers prepare for reduced water availability",
        paragraph1: "The food we eat, the water we drink...",
        mapperDiagram: {
            figurePath: "timeseries.png",
            caption: "Explore a map of current..."
        }        
    },
    WhenIsADroughtADrought: {
        title: "When is a drought a drought?",
        subtitle:"Percentiles tell us when low flows are streamflow droughts based on how often they occur",
        defineLowStreamflow: {
            heading: "Defining ‘unusually low’ streamflow using percentiles",
            paragraph1: "For any stream or river, defining ‘unusually low’ streamflow means understanding typical conditions throughout the year. For <a href='https://labs.waterdata.usgs.gov/visualizations/gages-through-the-ages/index.html' target='_blank'>stream gages</a> with at least 40 years of data, we have a good understanding of what streamflow levels are typically observed at that site.",
            paragraph2: "To understand how typical a mean daily streamflow value is, we can compare it to previous mean daily streamflow values on that same day of year in earlier years.",
            figure1Path: "percentiles_explainer_1.png",
            paragraph3: "We can then lump all of these values into percentile bins, based on how often they occur. For example, take an observed streamflow level of 4,800 cubic feet per second (cfs). If streamflow at the site is below 4,800 cfs on March 1<sup>st</sup> in 20% of recorded years, then 4,800 cfs is the 20<sup>th</sup> percentile streamflow for that site on that date. Another way to say it is that on March 1<sup>st</sup>, streamflow at that site is less than 4,800 cfs 20% of the time.  The USGS categorizes streamflow percentiles in the 10 – 25 percentile range as ‘below normal.’",
            figure2Path: "percentiles_explainer_2.png",
            paragraph4: "By doing this for every day of the year, we are able to place mean daily streamflow values in the context of historical observations.",
            figure3Path: "percentiles_explainer_3.png"
        },
        classifyStreamflowDrought: {
            heading: "Classifying streamflow drought using percentiles",
            paragraph1: "While the USGS streamflow categories shown above are useful for classifying all streamflow observed at a site, the low levels of streamflow that indicate streamflow drought are classified using <a href='https://droughtmonitor.unl.edu/About/AbouttheData/DroughtClassification.aspx' target='_blank'>U.S. Drought Monitor categories</a>. These categories bin low streamflow percentiles into specific drought categories that describe the intensity of the drought:",
            figurePath: "drought_percentiles_explainer.png",
            paragraph2: "For this project, we have specifically trained the model to forecast the following three categories of streamflow drought:<span><ul><li>Moderate drought (< 20<sup>th</sup> percentile)</li><li>Severe drought (< 10<sup>th</sup> percentile)</li><li>Extreme drought (< 5<sup>th</sup> percentile)</li></ul></span>"
        },
        accordionData: [
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
        subtitle:"Scientists train a model to accurately predict <i>low</i> streamflow percentiles",
        paragraph1: "To forecast streamflow drought at <a href='https://labs.waterdata.usgs.gov/visualizations/gages-through-the-ages/index.html' target='_blank'>USGS stream gages</a> across the contiguous United States (CONUS), we have built a machine learning model (a Long Short-Term Memory network, or LSTM) that predicts streamflow percentiles.",
        paragraph2: "To predict streamflow percentiles, we train the model with input data and output data for all of CONUS: <span><ul><li>Input data: <span class='tooltip-group'><span class='tooltip-span'>Watershed characteristics</span><span id='characteristics-tooltip' class='tooltiptext'>Some watershed characteristics that the model finds useful are average annual precipitation summaries, watershed elevation, and flowline slope. Many other characteristics are also provided, including land cover types, soil types, irrigation density (ditches, withdrawals, tile drainage), and transportation density (trails, roads, highways).</span></span>, antecedent precipitation and streamflow conditions, and upcoming weather forecasts</li><li>Output data: Streamflow percentiles at USGS stream gages. Because streamflow droughts occur when streamflow is unusually low, we specifically train the model to predict low streamflow percentiles by restricting the training dataset to observations below the 30th percentile</li></ul></span>",
        paragraph3: "Using cloud computing resources, the model is trained to “learn” the relationship between the input and output data.  After being trained on thousands of watersheds, the model learns that the same weather can lead to different relative streamflow conditions (streamflow percentiles) at different sites.",
        paragraph4: "We use the final CONUS-wide model to predict streamflow percentiles for all locations on select future dates and we convert the predicted percentiles to forecasts of streamflow drought using the established drought thresholds for moderate, severe, and extreme drought."
    },
    WhatDoForecastsLookLike: {
        title: "What do the forecasts look like?",
        subtitle: "The model generates weekly forecasts for 1-13 weeks in the future",
        forecastTimeseries: {
            paragraph1: "Every week, we ask the model to generate weekly forecasts for 1-13 weeks out. For each forecast horizon (e.g., 4 weeks out), the model produces a prediction (its best estimate of the streamflow percentile for each week) along with a 90% prediction interval that captures the uncertainty of the prediction. More on that piece later!",
            caption: "On each issue date, we generate forecasts for the next 13 weeks."
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
            paragraph1: "In order to evaluate how well the model performs, we can lump the predictions into four bins: <span><ul><li><span class='group-label true-neg'>True negatives</span>: the model did not predict drought, and no drought occurred</li><li><span class='group-label false-neg'>False negatives</span>: the model did not predict drought, but a drought occurred </li><li><span class='group-label true-pos'>True positives</span>: the model predicted drought, and a drought occurred</li><li><span class='group-label false-pos'>False positives</span>: the model predicted drought, but no drought occurred</li></ul></span>",
            paragraph2: "If we categorize all predictions that were generated for 1 week in the future, we see this:",
            caption1Desktop: "Hover your mouse over the Sankey plot to see how often the model predicts drought or not, and how often that prediction is correct (a ‘true’ outcome).",
            caption1Responsive: "Tap the Sankey plot to see how often the model predicts drought or not, and how often that prediction is correct (a ‘true’ outcome).",
            paragraph3: "Overall, the model does a good job of correctly predicting when streamflow drought will and will not occur 1 week in the future."
        },
        forecastTrueFalseSummary: {
            paragraph1: "As we generate forecasts for weeks that are further out, accuracy decreases:",
            caption: "Depending on the forecast horizon, the proportion of <span class='group-label true-neg'>true negatives</span>, <span class='group-label false-neg'>false negatives</span>, <span class='group-label false-pos'>false positives</span>, and <span class='group-label true-pos'>true positives</span> changes. More ‘false’ outcomes occur as the forecast horizon lengthens."
        },
        forecastTrueFalseRightOrWrong: {
            paragraph1: "Depending on what we’re interested in, we can look at different subsets of the results, where ‘right’ = ‘true’ outcomes, and ‘wrong’ = ‘false’ outcomes:",
            questionAll: "How often is the model <span class='group-label right'>right</span> or <span class='group-label wrong'>wrong</span>?",
            questionNoDrought: "If the model does not predict drought, how often is it <span class='group-label true-neg'>right</span> or <span class='group-label false-neg'>wrong</span>?",
            questionDrought: "If the model predicts drought, how often is it <span class='group-label true-pos'>right</span> or <span class='group-label false-pos'>wrong</span>?",
            caption: "Use the radio buttons to see how the overall model performance and how right or wrong the model is depending on whether it predicts drought or not. The model’s prediction ability is better with shorter forecast horizons."
        }
    },
    HowCaptureUncertainty: {
        title: "How does the model capture uncertainty?",
        subtitle:"Scientists train the model to provide a range of possible values",
        paragraph1: "When we forecast streamflow percentiles, we want to know the uncertainty associated with each prediction. To capture the uncertainty, we train the model to predict three things:<span><ul><li>The model’s best estimate of the streamflow percentile for each forecast date—this is the median prediction</li><li>The upper bound for the streamflow percentile—this is the 95% quantile. The model is predicting a value that is so high, given the current conditions, that we think it will only be exceeded 5% of the time</li><li>The lower bound for the streamflow percentile—this is the 5% quantile. The model is predicting a value that is so low, given the current conditions, that we think it will only be lower 5% of the time</li></ul></span>",
        paragraph2: "Essentially, we want the model to consider everything that could happen, given the current inputs, and give us the range of possible streamflow percentiles, excluding the 10% least likely scenarios.",
        paragraph3: "We set up the model to generate these three predicted values by using what are called loss functions.",
        lossFunctionDiagram: {
            heading: "Training models with loss functions",
            paragraph1: "Training an AI/ML model requires directing...",
            caption: "Loss functions use different rates of penalties for incorrect predictions depending on whether scientists are interested in the median, 95% quantile (upper bound), or 5% quantile (lower bound) values."
        },
        lossFunction: {
            paragraph1: "When we train the machine learning model, we incentivize it to find the best solution by penalizing it when it predicts incorrectly. In general, the more inaccurate the prediction, the higher the penalty. But some of the incorrect predictions may be overestimates, while some may be underestimates. Depending on what we are asking the model to predict, we want to penalize it differently for over- and under- estimations.",
            paragraph2: "To set the model up to generate the median prediction, we use a loss function that penalizes the model equally for under- and over- estimations. When plotted, this loss function has identical left and right slopes, so we call this a symmetric loss function. Incorrect predictions are penalized more the further they are from the actual value, regardless of whether they are over- or under- estimations.",
            paragraph3: "To set the model up to generate the upper bound prediction, we use a loss function that penalizes the model more steeply for under- estimating the actual value than for over-estimating it. When plotted, this loss function has a steeper left slope than right slope, so we call this an asymmetric loss function.",
            paragraph4: "To set the model up to generate the lower bound prediction, we do the opposite, using a loss function that penalizes the model more steeply for over-estimating the actual value. When plotted, this loss function is also asymmetric, with a steeper right slope than left slope.",
            paragraph5: "Explore the plot below to see how the asymmetry of the loss function influences model predictions:",
            caption2Desktop: "Hover your mouse in the gray region to see the relationship between the loss function (left) and the streamflow percentile prediction (right).",
            caption2Responsive: "Tap in the gray region to see the relationship between the loss function (left) and the streamflow percentile prediction (right).",
            paragraph6: "What do you see? When the left slope in the loss function is steeper than the right slope, the model favors high predictions, as we would expect. And the other way around, the model favors low predictions. This approach allows the model to bracket the range of its predictions, capturing the uncertainty."
        },
        predictionInterval: {
            heading: "Defining prediction intervals",
            paragraph1: "The upper and lower bounds that the model predicts define what we call the prediction interval. In this case, the model is predicting a 90% prediction interval. The percentage of the prediction interval tells us the approximate percentage of actual observations the model expects to be within the interval.",
            paragraph2: "You can see that the model does a good job of capturing the expected percent of observations if we specify different prediction intervals:",
            caption: "Use the radio buttons to explore the loss functions (left) and corresponding prediction intervals (right).",
            paragraph3: "Notice that the steeper the asymmetric loss functions, the wider the resulting prediction interval."
        }
    },
    WhatsNext: {
        title: "What comes next?",
        subtitle: "Continued work to improve the model and make it more useful",
        headingA: "Improvements to the model",
        paragraphA1: "In order to forecast streamflow drought, we have trained a model to predict when conditions will deviate from normal—when streamflow levels will become “unusually low”. This is much tricker than predicting typical streamflow, as the model cannot rely on historical conditions or seasonal patterns. To make the model more accurate, we hope to incorporate additional inputs, including <span class='tooltip-group'><span class='tooltip-span'>baseflow</span><span id='baseflow-tooltip' class='tooltiptext'>The portion of streamflow that is sustained primarily by groundwater discharge and is not due to runoff from precipitation or melting snow.</span></span> forecasts, better groundwater and soil water storage data, and a greater number of weather forecasts that are specialized for different forecast horizons.",
        headingB: "More ways to evaluate model performance",
        paragraphB1: "As the model continues to run, we will have a larger pool of predictions that we can use to evaluate model performance. In addition to determining the ability to accurately predict if streamflow drought will or will not occur, we will also assess if the model can accurately predict drought <i>events</i>. We want to know if the model accurately predicts when a drought will start (drought onset), how long it will last (drought duration), when it will end (drought termination), and how low the streamflow percentile will become (drought intensity). This is valuable information for water managers and communities that are preparing for drought conditions.",
        figureBpath: "drought_event_explainer.png",
        headingC: "Forecasts for more places",
        paragraphC1: "We are also expanding the model to generate forecasts for ungaged basins across CONUS.",
        paragraphC2: "Many regions <a href='https://www.usgs.gov/media/images/how-far-away-your-closest-streamgage' target='_blank'>lack sufficient streamflow monitoring stations</a>, making it challenging to manage water resources effectively. In many ungaged areas, there is limited historical data available for streamflow analysis. By applying our models to ungaged areas, we hope to better provide valuable information on water availability at management-relevant scales."
    },
    WhoContributing: {
        title: "Who is contributing to this project?",
        subtitle: "It’s a team effort",
        aboutTheTeam: {
            heading: "Collaboration across the USGS water community",
            paragraph1: "An interdisciplinary team of USGS researchers and data scientists are working together to forecast streamflow drought at a national scale.",
            paragraph2: "This is a collective effort by the <span class='group-label' data-group='OPP'>Office of Planning and Programming</span>, <span class='group-label' data-group='ESPD'>Earth Systems Processes Division</span>, <span class='group-label' data-group='IIDD'>Integrated Information Dissemination Division</span>, <span class='group-label' data-group='IMPD'>Integrated Modeling and Prediction Division</span>, <span class='group-label' data-group='OSD'>Observing Systems Division</span>, <span class='group-label' data-group='KS'>KS Water Science Center</span>, <span class='group-label' data-group='MD-DE-DC'>MD-DE-DC Water Science Center</span>, <span class='group-label' data-group='OR'>OR Water Science Center</span>, <span class='group-label' data-group='UT'>UT Water Science Center</span> and <span class='group-label' data-group='WY-MT'>WY-MT Water Science Center</span>."
        }
    },
    References: {
        title: "References"
    },
    Authors: {
        title: "USGS Vizlab"
    }
}
export default {
    pageTitle: "Modeling <span class='emph'>streamflow drought</span>",
    WhyForecastStreamflowDrought: {
        title: "Why model streamflow drought?",
        subtitle:"Streamflow drought forecasts help decision makers prepare for reduced water availability",
        paragraph1: "The food we eat, the water we drink, the clothes we buy, and the electricity we use depend on ample amounts of clean, accessible water. When water flowing through rivers and streams drops to unusually low levels—termed “<a href='https://water.usgs.gov/vizlab/what-is-drought/' target='_blank'>streamflow drought</a>”—water managers can have trouble allocating enough water to meet home, farm, business, and energy needs. To assist water managers, USGS developed Artificial Intelligence/Machine Learning (AI/ML) models that forecast streamflow drought up to 13 weeks (3 months) into the future. Streamflow drought forecasts help decision makers anticipate periods of limited water availability so they can develop plans for ensuring the safety and health of their communities.",
        mapperDiagram: {
            mapPathDesktop: "map_desktop.png",
            mapPathMobile: "map_mobile.png",
            caption: "Explore a map of current and forecast streamflow drought conditions across the lower 48 states and view detailed forecasts for individual sites on the <a href='https://water.usgs.gov/vizlab/streamflow-drought-forecasts/' target='_blank'>Streamflow drought assessment and forecasting tool</a>."
        }        
    },
    WhenIsADroughtADrought: {
        title: "When does low streamflow become a drought?",
        subtitle:"Percentiles tell us when low flows are streamflow droughts based on how often they occur",
        streamflowDroughtExample: {
            figurePath: "StreamflowDroughtExample.webp",
            caption: "Unusually low streamflow on the Peabody River in New Hampshire. Credit: John Hammond"
        },
        defineLowStreamflow: {
            heading: "Defining ‘unusually low’ streamflow using percentiles",
            paragraph1: "Knowing what is ‘unusual’ requires first knowing what is usual. For streamflow data, USGS scientists rely on <a href='https://labs.waterdata.usgs.gov/visualizations/gages-through-the-ages/index.html' target='_blank'>long-term historical records</a> collected at <a href='https://www.usgs.gov/mission-areas/water-resources/science/usgs-national-streamgaging-network' target='_blank'>thousands of USGS streamgage sites</a> across the United States. USGS scientists commonly summarize streamflow data into a mean daily value, which is the average streamflow for a single day. To understand how typical a mean daily streamflow value is, USGS scientists compare it to previous streamflow values on that same day in earlier years. The chart below shows the observed streamflow values on March 1<sup>st</sup> over 112 years at one USGS streamgage.",
            figure1Path: "percentile-01.png",
            paragraph2: "Streamflow values are categorized as normal, below normal, or above normal based on how often they occur. These frequency-based bins are called <span class ='emph'>percentiles</span>. For example, the observed streamflow at this site on April 12<sup>th</sup>, 2025, was 1,200 cubic feet per second (cfs, ~9,000 gallons per second). If streamflow at this site on April 12<sup>th</sup> is below 1,200 cfs in 20% of recorded years, then 1,200 cfs is the <span class ='emph'>20<sup>th</sup>-percentile streamflow</span> for that site on that date. Another way to say it is, at that site on April 12<sup>th</sup>, streamflow is less than 1,200 cfs 20% of the time. By calculating percentile values for every day of the year, we understand mean daily streamflow values in the context of historical observations. This would not be possible without the long-term historical record provided by the <a href='https://www.usgs.gov/mission-areas/water-resources/science/usgs-national-streamgaging-network' target='_blank'>USGS National Streamgaging network</a>.",
            figure2Path: "percentile-03.png",
        },
        classifyStreamflowDrought: {
            heading: "Classifying streamflow drought using percentiles",
            paragraph1: "While the USGS streamflow categories shown above are useful for classifying all streamflow observed at a site, the USGS is using the following U.S. Drought Monitor (USDM) categories to classify the low levels of streamflow that indicate streamflow drought:<span><ul><li>Moderate streamflow drought (10<sup>th</sup> - 20<sup>th</sup> percentile, USDM D1 drought)</li><li>Severe streamflow drought (5<sup>th</sup> - 10<sup>th</sup> percentile, USDM D2 drought)</li><li>Extreme streamflow drought (< 5<sup>th</sup> percentile, USDM D3 drought)</li></ul></span>",
            figurePath: "drought-example.png",
            paragraph2: "The U.S. Drought Monitor provides an additional category of drought below the 2<sup>nd</sup> percentile, termed exceptional drought (D4). For the data-driven models used to generate our streamflow drought forecasts, the sample of streamflow droughts below the 2<sup>nd</sup> percentile was too small to generate accurate models<u>,</u> so the lowest percentile-based category that the USGS is using is extreme streamflow drought."
        },
        accordionData: [
            {
                heading: "How are ‘low flows’ different from ‘streamflow drought’?",
                content: [
                    {
                        type: "text",
                        content: "‘Low streamflow’ does not always mean ‘streamflow drought.’ Low flows occur seasonally in many streams and are in line with typical conditions. In contrast, streamflow drought results when flows are unusually low compared to typical conditions."
                    },
                    {
                        type: "quote",
                        content: '"While droughts may include periods of low flows, a recurring seasonal low flow event is not necessarily a drought." – World Meteorological Organization, 2008'
                    }
                ],
                activeOnLoad: false
            }
        ],
        observationExplore: {
            paragraph1: "The plot below shows how streamflow at a site varies, dropping below normal and abnormally dry conditions to enter a streamflow drought.",
            caption1Desktop: "Hover your mouse over the plot to see when a stream goes into streamflow drought.",
            caption1Responsive: "Tap on the plot to see when a stream goes into streamflow drought.",
        },
    },
    HowModelStreamflowDrought: {
        title: "How does the USGS model streamflow drought?",
        subtitle:"Scientists train a machine learning model to accurately predict <i>low</i> streamflow percentiles",
        paragraph1: "To forecast streamflow drought at <a href='https://www.usgs.gov/mission-areas/water-resources/science/usgs-national-streamgaging-network' target='_blank'>USGS streamgages across the lower 48 states</a> (the conterminous United States, or CONUS), USGS scientists built an AI/ML (a long short-term memory, or LSTM, recurrent neural network) model that predicts streamflow percentiles. AI/ML can’t predict streamflow percentiles on its own—scientists must first train the model to learn the relationship between input and output data for thousands of watersheds across the country.",
        paragraph2: "<span><ul><li>Input data: <span class='tooltip-group'><span class='tooltip-span'>Watershed characteristics</span><span id='characteristics-tooltip' class='tooltiptext'>Some watershed characteristics that the model finds useful are average annual precipitation summaries, watershed elevation, and flowline slope. Many other characteristics are also provided, including land cover types, soil types, irrigation density (ditches, withdrawals, tile drainage), and transportation density (trails, roads, highways).</span></span>, recent precipitation and streamflow conditions, and upcoming weather forecasts</li><li>Output data: Streamflow percentiles at <a href='https://labs.waterdata.usgs.gov/visualizations/gages-through-the-ages/index.html' target='_blank'>USGS streamgages</a>. Because streamflow droughts occur when streamflow is unusually low, USGS scientists trained the model to accurately predict <i>low </i>streamflow percentiles by restricting the training dataset to observed streamflow values below the 30<sup>th</sup> percentile.</li></ul></span>",
        paragraph3: "Once the model is trained to accurately predict streamflow percentiles, USGS scientists convert the predicted percentiles for a site to forecasts of streamflow drought using the established streamflow drought thresholds for moderate, severe, and extreme streamflow drought.",
        paragraph4: "For more information on modeling methods please see the technical documentation (XXXX et al., 2025)."
    },
    WhatDoForecastsLookLike: {
        title: "What do the forecasts look like?",
        subtitle: "The model generates daily forecasts for 1-13 weeks in the future",
        forecastTimeseries: {
            paragraph1: "Every day, on what we call the ‘issue date’, the model generates streamflow drought forecasts for 1-13 weeks in the future. Each point in the future that receives a prediction is called a <span class ='emph'>forecast horizon</span>. For each forecast horizon, the model predicts its best estimate of the streamflow percentile for that week, along with a 90% prediction interval that captures the uncertainty of the prediction. More on that piece later!",
            caption: "On each issue date, we generate forecasts for the next 13 weeks."
        },
        forecastExplore: {
            paragraph1: "As noted above, the training dataset is restricted to observed streamflow values below the 30<sup>th</sup> percentile. This produces a trained model that does a good job of predicting the occurrence and severity of streamflow drought. But when the model predicts that streamflow drought will <i>not</i> occur, the streamflow percentile predicted by the model may be lower than what will actually be observed. This reduced accuracy at percentiles above the 30<sup>th</sup> percentile is a worthwhile tradeoff for improved accuracy at low streamflow percentiles, since this tool was developed to forecast streamflow drought.",
            paragraph2: "The USGS has also developed a second model that was trained on all percentiles. While this model is less accurate for predicting streamflow drought than the primary model trained on observed streamflow below the 30<sup>th</sup> percentile, it may be preferred by some users as its predictions more intuitively capture conditions when streamflow drought is not predicted.",
            paragraph3: "We can see how this model works and performs by comparing forecasts to observations at an example site. On the initial issue date, the model uses past streamflow conditions and other input data to make a forecast for the next 13 weeks. On the next issue date, the model updates its forecast by taking into account the most recent streamflow and precipitation data. The plot below overlays current and previous forecasts, showing how the model incorporates new data and updates its predictions.",
            caption1Desktop: "Hover your mouse over the plot to see how the model forecasts streamflow drought. For each issue date, the darkest line shows the current forecast. Previously generated forecasts are shown using faded lines, where the oldest forecasts are the faintest. The dotted line indicates the 30<sup>th</sup> percentile. The model is trained to accurately predict streamflow below this percentile. Anything below the 20th percentile is considered streamflow drought.",
            caption1Responsive: "Tap on the plot to see how the model forecasts streamflow drought. For each issue date, the darkest line shows the current forecast. Previously generated forecasts are shown using faded lines, where the oldest forecasts are the faintest. The dotted line indicates the 30<sup>th</sup> percentile. The model is trained to accurately predict streamflow below this percentile. Anything below the 20th percentile is considered streamflow drought.",
        }
    },
    HowWellModelPerform: {
        title: "How well does the model perform?",
        subtitle: "The model is more accurate in the near future than for longer forecast horizons",
        forecastTrueFalseSankey: {
            paragraph1: "To evaluate how well the model performs, we can group the predictions into four bins: <span><ul><li><span class='group-label true-neg'>True negatives</span>: the model did not predict streamflow drought, and no streamflow drought occurred</li><li><span class='group-label false-neg'>False negatives</span>: the model did not predict streamflow drought, but a streamflow drought occurred</li><li><span class='group-label true-pos'>True positives</span>: the model predicted streamflow drought, and a streamflow drought occurred</li><li><span class='group-label false-pos'>False positives</span>: the model predicted streamflow drought, but no streamflow drought occurred</li></ul></span>",
            paragraph2: "We can think of true negatives and positives as the model being right, and false negatives and positives as the model being wrong. The chart below shows the percentage of severe or extreme streamflow drought (&lt;<sup> </sup>10<sup>th</sup> percentile streamflow) predictions that fall into each of these categories when the model is forecasting streamflow drought one week into the future.",
            caption1Desktop: "Hover your mouse over the Sankey plot to see how often the model predicts </i>streamflow <i>drought or not, and how often that prediction is right (a ‘true’ outcome).",
            caption1Responsive: "Tap the Sankey plot to see how often the model predicts </i>streamflow <i>drought or not, and how often that prediction is right (a ‘true’ outcome).",
            paragraph3: "Overall, the model does a good job of correctly predicting when streamflow drought will and will not occur 1 week in the future."
        },
        forecastTrueFalseSummary: {
            paragraph1: "As we generate forecasts for weeks that are further out, accuracy decreases. In other words, we see more ‘false’ outcomes—where the model incorrectly predicts whether or not streamflow drought will occur—as the forecast horizon lengthens. Here is the accuracy breakdown for predictions of severe or extreme streamflow drought (&lt;<sup> </sup>10<sup>th</sup> percentile streamflow) for 1 through 13 weeks:",
            caption: "The proportion of true negatives, false negatives, false positives, and true positives changes with forecast horizon."
        },
        forecastTrueFalseRightOrWrong: {
            paragraph1: "With these results, we can evaluate model accuracy several different ways:",
            questionAll: "<span class ='emph'>Overall</span>, how often is the model <span class='group-label right'>right</span> or <span class='group-label wrong'>wrong</span>?",
            questionNoDrought: "If the model <span class ='emph'>does not predict streamflow drought</span>, how often is it <span class='group-label true-neg'>right</span> or <span class='group-label false-neg'>wrong</span>?",
            questionDrought: "If the model <span class ='emph'>does predict streamflow drought</span>, how often is it <span class='group-label true-pos'>right</span> or <span class='group-label false-pos'>wrong</span>?",
            caption: "Use the radio buttons to see the overall model performance and how right or wrong the model is depending on whether it predicts severe or extreme streamflow drought or not.",
            paragraph2: "Across the board, the model’s prediction ability is better with shorter forecast horizons."
        }
    },
    HowCaptureUncertainty: {
        title: "How does the model capture uncertainty?",
        subtitle:"Scientists train the model to provide a range of possible values",
        paragraph1: "To capture prediction uncertainty, USGS scientists train the model to predict three things:<span><ul><li>The model’s best estimate of the streamflow percentile for each forecast date—this is the <span class ='group-label median'>median prediction</span>. The model is predicting that, given the current conditions, there are equal odds (50-50) of the actual value being higher or lower than this predicted value.</li><li>The upper bound for the streamflow percentile—this is the <span class ='group-label q95'>95% quantile</span>. The model is predicting a value that is so high, given the current conditions, that we think it will only be exceeded 5% of the time.</li><li>The lower bound for the streamflow percentile—this is the <span class ='group-label q5'>5% quantile</span>. The model is predicting a value that is so low, given the current conditions, that we think it will only be lower 5% of the time.</li></ul></span>",
        paragraph2: "Essentially, scientists want the model to consider everything that could happen, given the current inputs, and provide the range of possible streamflow percentiles, excluding the 10% least likely scenarios. Note that, because the model is trained on observed streamflow <i>below</i> the 30<sup>th</sup> percentile, the model cannot accurately capture uncertainty <i>above</i> the 30<sup>th</sup> percentile. This is acceptable, since the priority is to accurately capture the uncertainty below the 30<sup>th</sup> percentile, when conditions would be in or near streamflow drought.",
        paragraph3: "The model generates these three predicted values by using what are called <span class ='emph'>loss functions</span>.",
        lossFunctionDiagram: {
            heading: "Training models with loss functions",
            paragraph1: "Training an AI/ML model requires directing it to the right solution. We do so by penalizing it when it predicts incorrectly. Some predictions may be overestimates, while others may be underestimates. Depending on the goal, different types of errors may warrant different penalties. In this case, because the model is trained on observed streamflow values below the 30<sup>th</sup> percentile, only predictions corresponding to observations below the 30<sup>th</sup> percentile are evaluated.",
            caption: "Loss functions use different rates of penalties for incorrect predictions depending on whether scientists are interested in the median, 95% quantile (upper bound), or 5% quantile (lower bound) values."
        },
        lossFunction: {
            paragraph1: "To generate a <span class ='group-label median'>median prediction</span>, scientists use a <span class ='emph'>symmetric loss function</span>. This function penalizes under- and overestimations equally. When plotted, the loss function has identical slopes on both sides of zero error—meaning penalties for incorrect predictions increase at the same rate whether the prediction is too high or too low.",
            paragraph2: "To generate a <span class ='group-label q95'>95% quantile prediction </span>(upper bound), scientists use an <span class ='emph'>asymmetric loss function</span> that penalizes underestimations more heavily than overestimations. This directional penalty results in a plot where the left slope (underestimate) is steeper than the right (overestimate).",
            paragraph3: "To generate a <span class ='group-label q5'>5% quantile prediction </span>(lower bound), the <span class ='emph'>asymmetric loss function</span> is reversed. Overestimates are penalized more than underestimates, producing a loss function with a steeper right slope.",
            paragraph4: "The plot below illustrates how different loss functions influence model predictions by changing the penalty applied to prediction errors.",
            captionDesktop: "Hover your mouse in the gray region on either chart to see the relationship between the loss function (left) and the 1-week streamflow percentile prediction (right). Use the toggles to highlight the loss function shapes and streamflow percentiles for the 95% quantile (upper bound), median, and 5% quantile (lower bound) predictions. Note that the training dataset restriction means the loss functions are only penalizing predictions corresponding to observations below the 30<sup>th</sup> percentile, and therefore best capture uncertainty for predictions in this range.",
            captionResponsive: "Tap in the gray region on either chart to see the relationship between the loss function (left) and the 1-week streamflow percentile prediction (right). Use the toggles to highlight the loss function shapes and streamflow percentiles for the 95% quantile (upper bound), median, and 5% quantile (lower bound) predictions. Note that the training dataset restriction means the loss functions are only penalizing predictions corresponding to observations below the 30<sup>th</sup> percentile, and therefore best capture uncertainty for predictions in this range.",
            paragraph5: "What do you see? When the left slope in the loss function is steeper than the right slope, meaning the function penalizes underestimation more strongly than overestimation, the model favors high predictions. Conversely, when the right slope is steeper than the left, the model favors low predictions. This approach allows the model to bracket the range of its predictions, capturing uncertainty in the forecast."
        },
        predictionInterval: {
            heading: "Defining prediction intervals",
            paragraph1: "The upper and lower bounds that the model predicts define what we call the <span class ='emph'>prediction interval</span> (PI for short). In this case, by excluding the 10% least likely prediction scenarios, the streamflow drought forecast model has a 90% prediction interval. The size of the prediction interval tells us the approximate percentage of actual observations <i>below the 30<sup>th</sup> percentile </i>the model expects to be within the interval. In other words, a 90% prediction interval should contain approximately 90% of observed streamflow values below the 30<sup>th</sup> percentile.",
            paragraph2: "The plot below shows that as the prediction interval increases, more observations are captured within the range of predictions. Moreover, by favoring underestimation and overestimation, steep asymmetric loss functions create wider prediction intervals than do loss functions with more equal slopes.",
            caption: "Use the radio buttons to explore the relationship between different prediction interval sizes (generated with a 1-week forecast horizon), loss functions (left), and % of observations below the 30<sup>th</sup> percentile captured within the prediction intervals (right)."
        }
    },
    WhatsNext: {
        title: "What comes next?",
        subtitle: "USGS continues to improve the model and make it more useful",
        headingA: "Continue to collaborate",
        paragraphA1: "Building on a series of <a href='https://www.drought.gov/documents/drought-prediction-and-water-availability-report-2022-usgs-nidis-national-listening' target='_blank'>listening sessions</a> co-organized and co-hosted with NOAA’s National Integrated Drought Information System (NIDIS) staffBuilding on a series of listening sessions co-organized and co-hosted with NOAA’s National Integrated Drought Information System (NIDIS) staff, USGS staff have been coordinating with other Federal Agencies and external partners to identify key drought research priorities. The goal of this collaboration is to develop and improve drought products and information at the national and regional scales in order to support decision-making. As these efforts continue, the USGS is committed to enhanced collaboration on priority drought research areas and drought related data collection.",
        headingB: "Continue to collect data",
        paragraphB1: "USGS streamgage data are foundational to being able to do this type of modeling. USGS will continue to operate the <a href='https://www.usgs.gov/mission-areas/water-resources/science/usgs-national-streamgaging-network' target='_blank'>National Streamgage Network</a> to maintain continuous records at streamgage sites across the U.S.",
        headingC: "Improvements to the model",
        paragraphC1: "USGS scientists hope to incorporate additional inputs to improve model accuracy. Potential new inputs include <span class='tooltip-group'><span class='tooltip-span'>baseflow</span><span id='baseflow-tooltip' class='tooltiptext'>The portion of streamflow that is sustained primarily by groundwater discharge and is not due to runoff from precipitation or melting snow.</span></span> forecasts, better groundwater and soil water storage data, and a greater number of weather forecasts that are specialized for different forecast horizons.",
        headingD: "More ways to evaluate model performance",
        paragraphD1: "As the model continues to run, USGS scientists can use the growing pool of predictions to evaluate model performance in new ways. Specifically, we can assess if the model accurately predicts when a streamflow drought event will start (streamflow drought onset), how long it will last (streamflow drought duration), when it will end (streamflow drought termination), and how low the streamflow percentile will become (streamflow drought intensity). This is valuable information for water managers and communities that are preparing for streamflow drought conditions.",
        figureDpath: "drought_event_explainer.png",
        headingE: "Forecasts for more places",
        paragraphE1: "USGS is also expanding the model to generate streamflow drought forecasts for CONUS basins that do not have streamgages. The <a href='https://www.usgs.gov/media/images/how-far-away-your-closest-streamgage' target='_blank'>lack of real-time and historical streamflow data</a> in these regions makes water management challenging for decision makers. By applying this streamflow drought forecast model to ungaged areas, USGS aims to provide valuable information on water availability at management-relevant scales.",
    },
    WhoContributing: {
        title: "Who is contributing to this project?",
        subtitle: "USGS scientists work together to model streamflow drought",
        aboutTheTeam: {
            heading: "Collaboration across the USGS water community",
            paragraph1: "An interdisciplinary team of USGS researchers and data scientists are working together to forecast streamflow drought at a national scale.",
            paragraph2: "This is a collective effort by the <span class='group-label' data-group='ESPD'>Earth Systems Processes Division</span>, <span class='group-label' data-group='IIDD'>Integrated Information Dissemination Division</span>, <span class='group-label' data-group='IMPD'>Integrated Modeling and Prediction Division</span>, <span class='group-label' data-group='OSD'>Observing Systems Division</span>, and <span class='group-label' data-group='OPP'>Office of Planning and Programming</span> within the USGS Water Resources Mission Area and the <span class='group-label' data-group='KS'>KS Water Science Center</span>, <span class='group-label' data-group='MD-DE-DC'>MD-DE-DC Water Science Center</span>, <span class='group-label' data-group='OR'>OR Water Science Center</span>, <span class='group-label' data-group='UT'>UT Water Science Center</span> and <span class='group-label' data-group='WY-MT'>WY-MT Water Science Center</span>."
        }
    },
    References: {
        title: "References"
    },
    Authors: {
        title: "USGS Vizlab"
    }
}


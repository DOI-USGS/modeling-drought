<template>
    <VizSection
        id="forecast"
        :figures="true"
        :fig-caption="true"
    >
        <!-- HEADING -->
        <template #heading>
            <h2>
                {{ text.heading }}
            </h2>
        </template>
        <!-- FIGURES -->
        <template #aboveExplanation>
            <p v-html="text.paragraph1" />
            <p v-html="text.paragraph2" />
        </template>

        <!-- Is this the simplest way to set an image? -->
        <template #figures>
            <div id="forecast-grid-container">
                <forecastPlot
                    id="forecast-svg"
                />
            </div>
        </template>
        <!-- FIGURE CAPTION -->
        <template #figureCaption>
        <p v-html="text.caption" />
        </template>
        <!-- EXPLANATION -->
        <template #belowExplanation>
            <p v-html="text.paragraph3" />
        </template>
    </VizSection>
</template>

<script setup>
    import { onMounted } from "vue";
    import * as d3 from 'd3';
    import VizSection from '@/components/VizSection.vue';
    import forecastPlot from "@/assets/svgs/forecast.svg";

    // define props
    defineProps({
        text: { type: Object }
    })

    // Declare behavior on mounted
    // functions called here
    onMounted(() => {
        addInteractions();
    });
    
    function mouseover(event) {
        if (event.currentTarget.id.startsWith("forecast_hover_")){
            let line_id = event.currentTarget.id.slice(15);
            //forecast lines
            d3.select("#forecast_lower_" + line_id).selectAll("path")
                .style("stroke-opacity", 1)
            d3.select("#forecast_middl_" + line_id).selectAll("path")
                .style("stroke-opacity", 1)
            d3.select("#forecast_patch_" + line_id).selectAll("path")
                .style("fill", d3.rgb(0,0,0,0.1))
            d3.select("#forecast_upper_" + line_id).selectAll("path")
                .style("stroke-opacity", 1)
            //prediction lines
            d3.select("#prediction_lower_" + line_id).selectAll("path")
                .style("stroke-opacity", 1)
            d3.select("#prediction_middl_" + line_id).selectAll("path")
                .style("stroke-opacity", 1)
            d3.select("#prediction_patch_" + line_id).selectAll("path")
                .style("fill", d3.rgb(0,0,0,0.2))
            d3.select("#prediction_upper_" + line_id).selectAll("path")
                .style("stroke-opacity", 1)
        }
      }

    function mouseout(event) {
        if (event.currentTarget.id.startsWith("forecast_hover_")){
            let line_id = event.currentTarget.id.slice(15);
            d3.select("#forecast_lower_" + line_id).selectAll("path")
                .style("stroke-opacity", 0)
            d3.select("#forecast_middl_" + line_id).selectAll("path")
                .style("stroke-opacity", 0)
            d3.select("#forecast_patch_" + line_id).selectAll("path")
                .style("fill", d3.rgb(0,0,0,0))
            d3.select("#forecast_upper_" + line_id).selectAll("path")
                .style("stroke-opacity", 0)
            //prediction lines
            d3.select("#prediction_lower_" + line_id).selectAll("path")
                .style("stroke-opacity", 0)
            d3.select("#prediction_middl_" + line_id).selectAll("path")
                .style("stroke-opacity", 0)
            d3.select("#prediction_patch_" + line_id).selectAll("path")
                .style("fill", d3.rgb(0,0,0,0))
            d3.select("#prediction_upper_" + line_id).selectAll("path")
                .style("stroke-opacity", 0)
        }
    }

    function click(event) {
        if (event.currentTarget.id.startsWith("OBSERVED-TAG")){
            //observation line toggle
            let observation_opacity = 0.5
            if (d3.select("#observation_full").selectAll("path").style("stroke-opacity") == 0){
                d3.select("#observation_full").selectAll("path")
                    .style("stroke-opacity", observation_opacity)
            } else if (d3.select("#observation_full").selectAll("path").style("stroke-opacity") == observation_opacity){
                d3.select("#observation_full").selectAll("path")
                    .style("stroke-opacity", 0)
            }
        }
    }

    function addInteractions() {
        // set viewbox for svg with loss function chart
        const forecastSVG = d3.select("#forecast-svg")

        // Add interaction to loss function chart
        forecastSVG.selectAll("g")
            .on("mouseover", (event) => mouseover(event))
            .on("mouseout", (event) => mouseout(event))
            .on("click", (event) => click(event))
    }
</script>

<style scoped lang="scss">
    #forecast-grid-container {
        display: grid;
        width: 100%;
        max-width: 1200px;
        margin: 0 auto 0 auto;
        grid-template-areas:
            "chart";
    }
    #forecast-svg {
        grid-area: chart;
        place-self: center;
        max-height: 80%;
        max-width: 80%;
    }
</style>
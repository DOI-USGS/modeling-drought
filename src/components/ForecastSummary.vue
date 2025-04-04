<template>
    <VizSection
        id="forecast-summary"
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
        </template>


        <!-- Is this the simplest way to set an image? -->
        <template #figures>
            <div id="fc-grid-container">
                <fcPlot
                    id="fc-svg"
                />
            </div>
            <div id="fcwd-grid-container">
                <fcwdPlot
                    id="fcwd-svg"
                />
            </div>
        </template>
        <!-- FIGURE CAPTION -->
        <template #figureCaption>
        <p v-html="text.caption" />
        </template>

    </VizSection>
</template>

<script setup>
    import { onMounted } from "vue";
    import * as d3 from 'd3';
    import VizSection from '@/components/VizSection.vue';
    import fcPlot from "@/assets/svgs/fc_summary.svg";
    import fcwdPlot from "@/assets/svgs/fc_wd_summary.svg";

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
        if (event.currentTarget.id.startsWith("drought-forecast-summary")){
            d3.select("#drought-forecast-summary-patch").selectAll("path")
                .style("fill-opacity", 0.5);
            d3.select("#drought-forecast-summary-line").selectAll("path")
                .style("stroke-opacity", 0.75);
        }
        if (event.currentTarget.id.startsWith("wet-forecast-summary")){
            d3.select("#wet-forecast-summary-patch").selectAll("path")
                .style("fill-opacity", 0.5);
            d3.select("#wet-forecast-summary-line").selectAll("path")
                .style("stroke-opacity", 0.75);
        }
      }

    function mouseout(event) {
        if (event.currentTarget.id.startsWith("drought-forecast-summary")){
            d3.select("#drought-forecast-summary-patch").selectAll("path")
                .style("fill-opacity", 0.15);
            d3.select("#drought-forecast-summary-line").selectAll("path")
                .style("stroke-opacity", 0.15);
        }
        if (event.currentTarget.id.startsWith("wet-forecast-summary")){
            d3.select("#wet-forecast-summary-patch").selectAll("path")
                .style("fill-opacity", 0.15);
            d3.select("#wet-forecast-summary-line").selectAll("path")
                .style("stroke-opacity", 0.15);
        }
      }

    function addInteractions() {
        // set viewbox for svg with confidence interval chart
        const fcwdSVG = d3.select("#fcwd-svg")

        // Add interaction to confidence interval chart
        fcwdSVG.selectAll("g")
            .on("mouseover", (event) => mouseover(event))
            .on("mouseout", (event) => mouseout(event))
    }
</script>

<style scoped lang="scss">
    #fc-grid-container {
        display: grid;
        width: 100%;
        max-width: 800px;
        margin: 3rem auto 4rem auto;
        grid-template-areas:
            "chart";
    }
    #fc-svg {
        grid-area: chart;
        place-self: center;
        height: 100%;
        width: 100%;
    }
    #fcwd-grid-container {
        display: grid;
        width: 100%;
        max-width: 800px;
        margin: 3rem auto 4rem auto;
        grid-template-areas:
            "chart";
    }
    #fcwd-svg {
        grid-area: chart;
        place-self: center;
        height: 100%;
        width: 100%;
    }
</style>
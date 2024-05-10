<template>
    <VizSection
        id="confidence-interval"
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
            <div id="region-grid-container">
                <ciPlot
                    id="ci-svg"
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
    import { onMounted, ref } from "vue";
    import * as d3 from 'd3';
    import VizSection from '@/components/VizSection.vue';
    import ciPlot from "@/assets/svgs/ci_example.svg";

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
        if (event.currentTarget.parentNode.id.startsWith("TAG")){
            var tag_id = event.currentTarget.parentNode.id;
            d3.select(document.getElementById(tag_id + " BOLD")).selectAll("g")
                .style("opacity",1);
            d3.select(document.getElementById(tag_id + " LABEL BOLD")).selectAll("g")
                .style("opacity",1);
            var line_id = event.currentTarget.parentNode.id.slice(4);
            d3.select(document.getElementById("CI PATCH " + line_id)).selectAll("path")
                .attr("r", 100)
                .style("fill-opacity",0.5)
                .style("stroke-opacity",0.5);
            d3.select(document.getElementById("CI PATCH LOWER " + line_id)).selectAll("path")
                .attr("r", 100)
                .style("stroke-opacity",1);
            d3.select(document.getElementById("CI PATCH UPPER " + line_id)).selectAll("path")
                .attr("r", 100)
                .style("stroke-opacity",1);
            d3.select(document.getElementById("LF LOWER " + line_id)).selectAll("path")
                .attr("r", 100)
                .style("stroke-opacity",1);
            d3.select(document.getElementById("LF UPPER " + line_id)).selectAll("path")
                .attr("r", 100)
                .style("stroke-opacity",1);
        }
      }

    function mouseout(event) {
        if (event.currentTarget.parentNode.id.startsWith("TAG")){
            var tag_id = event.currentTarget.parentNode.id;
            d3.select(document.getElementById(tag_id + " BOLD")).selectAll("g")
                .style("opacity",0);
            d3.select(document.getElementById(tag_id + " LABEL BOLD")).selectAll("g")
                .style("opacity",0);
            var line_id = event.currentTarget.parentNode.id.slice(4);
            d3.select(document.getElementById("CI PATCH " + line_id)).selectAll("path")
                .attr("r", 100)
                .style("fill-opacity",0)
                .style("stroke-opacity",0);
            d3.select(document.getElementById("CI PATCH LOWER " + line_id)).selectAll("path")
                .attr("r", 100)
                .style("stroke-opacity",0);
            d3.select(document.getElementById("CI PATCH UPPER " + line_id)).selectAll("path")
                .attr("r", 100)
                .style("stroke-opacity",0);
            d3.select(document.getElementById("LF LOWER " + line_id)).selectAll("path")
                .attr("r", 100)
                .style("stroke-opacity",0);
            d3.select(document.getElementById("LF UPPER " + line_id)).selectAll("path")
                .attr("r", 100)
                .style("stroke-opacity",0);
        }
    }
    function addInteractions() {
        // set viewbox for svg with wedges
        const lfSVG = d3.select("#ci-svg")

        // Add interaction to wedges
        lfSVG.selectAll("g")
            .on("mouseover", (event) => mouseover(event))
            .on("mouseout", (event) => mouseout(event))
    }
</script>

<style scoped lang="scss">
    // What is the best way to set this up?
    #region-grid-container {
        display: grid;
        width: 100%;
        max-width: 1200px;
        grid-template-areas:
            "chart";
    }
    #ci-svg {
        grid-area: chart;
        place-self: center;
        max-height: 80%;
        max-width: 80%;
    }
</style>
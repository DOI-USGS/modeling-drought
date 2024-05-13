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
            <div id="ci-grid-container">
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
    import { onMounted } from "vue";
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
        if (event.currentTarget.id.startsWith("TAG")){
            let tag_id = event.currentTarget.id;
            d3.select(document.getElementById(tag_id)).selectAll("text")
                .style("font-weight", 700);
            d3.select(document.getElementById(tag_id + "-LABEL-BOLD")).selectAll("text")
                .style("opacity", 1);
            let line_id = event.currentTarget.id.slice(4);
            d3.select(document.getElementById("CI-PATCH-" + line_id)).selectAll("path")
                .style("fill-opacity", 0.5)
                .style("stroke-opacity", 0.5);
            d3.select(document.getElementById("CI-PATCH-LOWER-" + line_id)).selectAll("path")
                .style("stroke-opacity", 1);
            d3.select(document.getElementById("CI-PATCH-UPPER-" + line_id)).selectAll("path")
                .style("stroke-opacity", 1);
            d3.select(document.getElementById("LF-LOWER-" + line_id)).selectAll("path")
                .style("stroke-opacity", 1);
            d3.select(document.getElementById("LF-UPPER-" + line_id)).selectAll("path")
                .style("stroke-opacity", 1);
        }
      }

    function mouseout(event) {
        if (event.currentTarget.id.startsWith("TAG")){
            let tag_id = event.currentTarget.id;
            d3.select(document.getElementById(tag_id)).selectAll("text")
                .style("font-weight", 400);
            d3.select(document.getElementById(tag_id + "-LABEL-BOLD")).selectAll("text")
                .style("opacity", 0);
            let line_id = event.currentTarget.id.slice(4);
            d3.select(document.getElementById("CI-PATCH-" + line_id)).selectAll("path")
                .style("fill-opacity", 0)
                .style("stroke-opacity", 0);
            d3.select(document.getElementById("CI-PATCH-LOWER-" + line_id)).selectAll("path")
                .style("stroke-opacity", 0);
            d3.select(document.getElementById("CI-PATCH-UPPER-" + line_id)).selectAll("path")
                .style("stroke-opacity", 0);
            d3.select(document.getElementById("LF-LOWER-" + line_id)).selectAll("path")
                .style("stroke-opacity", 0);
            d3.select(document.getElementById("LF-UPPER-" + line_id)).selectAll("path")
                .style("stroke-opacity", 0);
        }
    }
    function addInteractions() {
        // set viewbox for svg with confidence interval chart
        const lfSVG = d3.select("#ci-svg")

        // Add interaction to confidence interval chart
        lfSVG.selectAll("g")
            .on("mouseover", (event) => mouseover(event))
            .on("mouseout", (event) => mouseout(event))
    }
</script>

<style scoped lang="scss">
    #ci-grid-container {
        display: grid;
        width: 100%;
        max-width: 1200px;
        margin: 0 auto 0 auto;
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
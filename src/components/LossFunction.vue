<template>
    <VizSection
        id="loss-function"
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
            <div id="region-grid-container">
                <lfPlot
                    id="lf-svg"
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
    import { onMounted, ref } from "vue";
    import * as d3 from 'd3';
    import VizSection from '@/components/VizSection.vue';
    import lfPlot from "@/assets/svgs/lf_example.svg";

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
        if (event.currentTarget.id.startsWith("LF")){
            d3.select(event.currentTarget).selectAll("path")
                .attr("r", 100)
                .style("stroke-opacity",1)
                .style("stroke",d3.rgb(0,0,0));
            var line_id = event.currentTarget.id.slice(3);
            d3.select(document.getElementById("FORECAST " + line_id)).selectAll("path")
                .attr("r", 100)
                .style("stroke-opacity",1)
                .style("stroke",d3.rgb(0,0,0));
        }
        if (event.currentTarget.id.startsWith("FORECAST")){
            d3.select(event.currentTarget).selectAll("path")
                .attr("r", 100)
                .style("stroke-opacity",1)
                .style("stroke",d3.rgb(0,0,0));
            var line_id = event.currentTarget.id.slice(9);
            d3.select(document.getElementById("LF " + line_id)).selectAll("path")
                .attr("r", 100)
                .style("stroke-opacity",1)
                .style("stroke",d3.rgb(0,0,0));
        }
        if (event.currentTarget.parentNode.id.endsWith(" TAG")){
            var tag_id = event.currentTarget.parentNode.id;
            d3.select(document.getElementById(tag_id + " BOLD")).selectAll("g")
                .style("opacity",1);
            var line_id = event.currentTarget.parentNode.id.slice(0, -4);
            d3.select(document.getElementById(line_id + " FORECAST LINE")).selectAll("path")
                .attr("r", 100)
                .style("stroke-opacity",1);
            d3.select(document.getElementById(line_id + " LF LINE")).selectAll("path")
                .attr("r", 100)
                .style("stroke-opacity",1);
        }
      }

    function mouseout(event) {
        if (event.currentTarget.id.startsWith("LF")){
            d3.select(event.currentTarget).selectAll("path")
                .attr("r", 100)
                .style("stroke-opacity",0)
                .style("stroke",d3.rgb(0,0,0));
            var line_id = event.currentTarget.id.slice(3);
            d3.select(document.getElementById("FORECAST " + line_id)).selectAll("path")
                .attr("r", 100)
                .style("stroke-opacity",0)
                .style("stroke",d3.rgb(0,0,0));
        }
        if (event.currentTarget.id.startsWith("FORECAST")){
            d3.select(event.currentTarget).selectAll("path")
                .attr("r", 100)
                .style("stroke-opacity",0)
                .style("stroke",d3.rgb(0,0,0));
            var line_id = event.currentTarget.id.slice(9);
            d3.select(document.getElementById("LF " + line_id)).selectAll("path")
                .attr("r", 100)
                .style("stroke-opacity",0)
                .style("stroke",d3.rgb(0,0,0));
      }
        if (event.currentTarget.parentNode.id.endsWith(" TAG")){
            var tag_id = event.currentTarget.parentNode.id;
            d3.select(document.getElementById(tag_id + " BOLD")).selectAll("g")
                .style("opacity",0);
            var line_id = event.currentTarget.parentNode.id.slice(0, -4);
            d3.select(document.getElementById(line_id + " FORECAST LINE")).selectAll("path")
                .attr("r", 100)
                .style("stroke-opacity",0);
            d3.select(document.getElementById(line_id + " LF LINE")).selectAll("path")
                .attr("r", 100)
                .style("stroke-opacity",0);
        }
    }
    function addInteractions() {
        // set viewbox for svg with wedges
        const lfSVG = d3.select("#lf-svg")

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
    #lf-svg {
        grid-area: chart;
        place-self: center;
        max-height: 80%;
        max-width: 80%;
    }
</style>
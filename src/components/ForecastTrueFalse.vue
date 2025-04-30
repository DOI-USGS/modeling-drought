<template>
  <VizSection
    id="forecast-true-false"
    :figures="true"
    :fig-caption="true"
  >
    <!-- HEADING -->
    <template #heading>
      <h3>
        {{ text.heading }}
      </h3>
    </template>
    <template #aboveExplanation>
      <p v-html="text.paragraph1" />
    </template>
    <!-- FIGURES -->
    <template #figures>
      <div id="fc-true-false-grid-container">
        <fckeyPlot
          id="fc-true-false-svg"
        />
      </div>
      <div id="fc-true-false-sum-grid-container">
        <fcsumPlot
          id="fc-true-false-sum-svg"
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
    import fckeyPlot from "@/assets/svgs/fc_tf_key_desktop.svg";
    import fcsumPlot from "@/assets/svgs/fc_tf_sum_desktop.svg";

    // define props
    defineProps({
        text: { 
            type: Object,
            default() {
                return {}
            } 
        }
    })

    // Declare behavior on mounted
    // functions called here
    onMounted(() => {
        addInteractions();
    });
    

    // Draw the percent width line and label
    function draw_sankey(tf_id) {
        d3.select("#tf-bar-" + tf_id).selectAll("path")
            .style("fill-opacity", 1)
        d3.select("#tf-swoop-" + tf_id).selectAll("path")
            .style("fill-opacity", 0.2)
        d3.select("#tf-label-" + tf_id).selectAll("text")
            .style("opacity", 1);
    }

    // Draw the percent width line and label
    function remove_sankey(tf_id) {
        d3.select("#tf-bar-" + tf_id).selectAll("path")
            .style("fill-opacity", 0.25)
        d3.select("#tf-swoop-" + tf_id).selectAll("path")
            .style("fill-opacity", 0.05)
        d3.select("#tf-label-" + tf_id).selectAll("text")
            .style("opacity", 0.0);
    }

    function mouseover(event) {
      if (event.currentTarget.id.startsWith("tf-bar-")){
            let tf_id = event.currentTarget.id.slice(7);
            draw_sankey(tf_id);
            if (tf_id.length > 2){
              draw_sankey(tf_id.slice(0,-3));
              console.log(tf_id)
            }
        }
      else if (event.currentTarget.id.startsWith("tf-label-")){
            let tf_id = event.currentTarget.id.slice(9);
            draw_sankey(tf_id);
            if (tf_id.length > 2){
              draw_sankey(tf_id.slice(0,-3));
            }
        }
      else if (event.currentTarget.id.startsWith("tf-swoop-")){
            let tf_id = event.currentTarget.id.slice(9);
            draw_sankey(tf_id);
            if (tf_id.length > 2){
              draw_sankey(tf_id.slice(0,-3));
            }
        }
      }

    function mouseout(event) {
      if (event.currentTarget.id.startsWith("tf-bar-")){
            let tf_id = event.currentTarget.id.slice(7);
            remove_sankey(tf_id);
            if (tf_id.length > 2){
              remove_sankey(tf_id.slice(0,-3));
            }
        }
      else if (event.currentTarget.id.startsWith("tf-label-")){
            let tf_id = event.currentTarget.id.slice(9);
            remove_sankey(tf_id);
            if (tf_id.length > 2){
              remove_sankey(tf_id.slice(0,-3));
            }
        }
      else if (event.currentTarget.id.startsWith("tf-swoop-")){
            let tf_id = event.currentTarget.id.slice(9);
            remove_sankey(tf_id);
            if (tf_id.length > 2){
              remove_sankey(tf_id.slice(0,-3));
            }
        }
      }

    function addInteractions() {
        // set viewbox for svg with confidence interval chart
        const fckeySVG = d3.select("#fc-true-false-svg")
        // Add interaction to confidence interval chart
        fckeySVG.selectAll("g")
            .on("mouseover", (event) => mouseover(event))
            .on("mouseout", (event) => mouseout(event))
    }
</script>

<style scoped lang="scss">
    #fc-true-false-grid-container {
        display: grid;
        width: 100%;
        max-width: 800px;
        margin: 3rem auto 4rem auto;
        grid-template-areas:
            "chart";
    }
    #fc-true-false-svg {
        grid-area: chart;
        place-self: center;
        height: 100%;
        width: 100%;
    }
    #fc-true-false-sum-grid-container {
        display: grid;
        width: 100%;
        max-width: 800px;
        margin: 3rem auto 4rem auto;
        grid-template-areas:
            "chart";
    }
    #fc-true-false-sum-svg {
        grid-area: chart;
        place-self: center;
        height: 100%;
        width: 100%;
    }
</style>
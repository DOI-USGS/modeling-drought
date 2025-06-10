<template>
  <VizSection
    id="forecast-true-false"
    :figures="true"
    :fig-caption="true"
  >
    <template #aboveExplanation>
      <p v-html="text.paragraph1" />
    </template>
    <!-- FIGURES -->
    <template #figures>
      <div id="fc-true-false-sum-grid-container">
        <fcsumTFPlotTablet
          v-if="tabletView"
          id="fc-true-false-sum-svg"
        />
        <fcsumTFPlotMobile
          v-else-if="mobileView"
          id="fc-true-false-sum-svg"
        />
        <fcsumTFPlotDesktop
          v-else
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
    import { isMobileOnly } from 'mobile-device-detect';
    import { isTablet } from 'mobile-device-detect';
    import VizSection from '@/components/VizSection.vue';
    import fcsumTFPlotDesktop from "@/assets/svgs/fc_tf_sum_desktop.svg";
    import fcsumTFPlotTablet from "@/assets/svgs/fc_tf_sum_tablet.svg";
    import fcsumTFPlotMobile from "@/assets/svgs/fc_tf_sum_mobile.svg";

    // global variables
    const mobileView = isMobileOnly;
    const tabletView = isTablet;

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
    #fc-true-false-sum-grid-container {
        display: grid;
        width: 100%;
        max-width: 800px;
        margin: 2rem auto 0rem auto;
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
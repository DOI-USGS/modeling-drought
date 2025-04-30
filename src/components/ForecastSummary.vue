<template>
  <VizSection
    id="forecast-summary"
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
      <div id="fc-summary-grid-container">
        <fcsumPlot
          id="fc-summary-svg"
        />
      </div>
    </template>
    <!-- FIGURE CAPTION -->
    <template #figureCaption>
      <p v-if="tabletView" v-html="text.caption1Responsive" />
      <p v-else-if="mobileView" v-html="text.caption1Responsive" />
      <p v-else v-html="text.caption1Desktop" />
    </template>
  </VizSection>
</template>

<script setup>
    import { onMounted } from "vue";
    import * as d3 from 'd3';
    import { isMobile } from 'mobile-device-detect';
    import { isTablet } from 'mobile-device-detect';
    import VizSection from '@/components/VizSection.vue';
    import fcsumPlot from "@/assets/svgs/fc_summary_desktop.svg";

    // global variables
    const mobileView = isMobile;
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
    function drew_prediction_width(pw_id) {
        d3.select("#prediction-width-line-" + pw_id).selectAll("path")
            .style("stroke-opacity", 1)
        d3.select("#prediction-width-label-percent-" + pw_id).selectAll("text")
            .style("opacity", 1);
    }

    // Draw the percent width line and label
    function remove_prediction_width(pw_id) {
        d3.select("#prediction-width-line-" + pw_id).selectAll("path")
            .style("stroke-opacity", 0)
        d3.select("#prediction-width-label-percent-" + pw_id).selectAll("text")
            .style("opacity", 0);
    }

    function mouseover(event) {
      if (event.currentTarget.id.startsWith("prediction-width-hover")){
            let pw_id = event.currentTarget.id.slice(23);
            drew_prediction_width(pw_id);
        }
      }

    function mouseout(event) {
      if (event.currentTarget.id.startsWith("prediction-width-hover")){
            let pw_id = event.currentTarget.id.slice(23);
            remove_prediction_width(pw_id);
        }
      }

    function addInteractions() {
        // set viewbox for svg with confidence interval chart
        const fcsumSVG = d3.select("#fc-summary-svg")
        // Add interaction to confidence interval chart
        fcsumSVG.selectAll("g")
            .on("mouseover", (event) => mouseover(event))
            .on("mouseout", (event) => mouseout(event))
    }
</script>

<style scoped lang="scss">
    #fc-summary-grid-container {
        display: grid;
        width: 100%;
        max-width: 800px;
        margin: 3rem auto 4rem auto;
        grid-template-areas:
            "chart";
    }
    #fc-summary-svg {
        grid-area: chart;
        place-self: center;
        height: 100%;
        width: 100%;
    }
</style>
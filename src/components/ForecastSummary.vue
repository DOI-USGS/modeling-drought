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
        <svg width="0" height="0">
          <filter id="outline">
              <feMorphology in="SourceAlpha" result="DILATED" operator="dilate" radius="2"></feMorphology>
              
              <feFlood flood-color="#FFFFFF" flood-opacity="1" result="PINK"></feFlood>
              <feComposite in="PINK" in2="DILATED" operator="in" result="OUTLINE"></feComposite>
              
              <feMerge>
                    <feMergeNode in="OUTLINE" />
                    <feMergeNode in="SourceGraphic" />
              </feMerge>
        </filter>
        </svg>
        <svg width="0" height="0">
          <filter id="outline-light">
              <feMorphology in="SourceAlpha" result="DILATED" operator="dilate" radius="1"></feMorphology>
              
              <feFlood flood-color="#FFFFFF" flood-opacity="1" result="PINK"></feFlood>
              <feComposite in="PINK" in2="DILATED" operator="in" result="OUTLINE"></feComposite>
              
              <feMerge>
                    <feMergeNode in="OUTLINE" />
                    <feMergeNode in="SourceGraphic" />
              </feMerge>
        </filter>
        </svg>
        <fcsumPlotTablet
          v-if="tabletView"
          id="fc-summary-svg"
        />
        <fcsumPlotMobile
          v-else-if="mobileView"
          id="fc-summary-svg"
        />
        <fcsumPlotDesktop
          v-else
          id="fc-summary-svg"
        />
      </div>
    </template>
    <!-- FIGURE CAPTION -->
    <template #figureCaption>
      <p
        v-if="tabletView"
        v-html="text.caption1Responsive"
      />
      <p
        v-else-if="mobileView"
        v-html="text.caption1Responsive"
      />
      <p
        v-else
        v-html="text.caption1Desktop"
      />
    </template>
  </VizSection>
</template>


<script setup>
    import { onMounted } from "vue";
    import * as d3 from 'd3';
    import { isMobileOnly } from 'mobile-device-detect';
    import { isTablet } from 'mobile-device-detect';
    import VizSection from '@/components/VizSection.vue';
    import fcsumPlotDesktop from "@/assets/svgs/fc_summary_desktop.svg";
    import fcsumPlotMobile from "@/assets/svgs/fc_summary_mobile.svg";
    import fcsumPlotTablet from "@/assets/svgs/fc_summary_tablet.svg";

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
    function draw_prediction_width(pw_id) {
        d3.select("#prediction-width-line-" + pw_id).selectAll("path")
            .style("stroke-opacity", 1)
        d3.select("#prediction-width-label-week-" + pw_id).selectAll("text")
            .style("opacity", 1);
        d3.select("#prediction-width-label-lower-percentile-" + pw_id).selectAll("text")
            .style("opacity", 1)
            .attr("filter", "url(#outline-light)"); // Apply the glow filter;
        d3.select("#prediction-width-label-upper-percentile-" + pw_id).selectAll("text")
            .style("opacity", 1)
            .attr("filter", "url(#outline-light)"); // Apply the glow filter;
    }

    // Draw the percent width line and label
    function remove_prediction_width(pw_id) {
        d3.select("#prediction-width-line-" + pw_id).selectAll("path")
            .style("stroke-opacity", 0)
        d3.select("#prediction-width-label-week-" + pw_id).selectAll("text")
            .style("opacity", 0);
        d3.select("#prediction-width-label-lower-percentile-" + pw_id).selectAll("text")
            .style("opacity", 0);
        d3.select("#prediction-width-label-upper-percentile-" + pw_id).selectAll("text")
            .style("opacity", 0);
    }

    function mouseover(event) {
      if (event.currentTarget.id.startsWith("prediction-width-hover")){
            let pw_id = event.currentTarget.id.slice(23);
            draw_prediction_width(pw_id);
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

        d3.select("#prediction-interval-median-label").selectAll("text")
            .attr("filter", "url(#outline)"); // Apply the glow filter;
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
<template>
  <VizSection
    id="forecast-true-false"
    :figures="true"
    :fig-caption="true"
  >
    <template #aboveExplanation>
      <p v-html="text.paragraph1" />
      <p v-html="text.paragraph2" />
    </template>
    <!-- FIGURES -->
    <template #figures>
      <div id="fc-true-false-grid-container">
        <fckeyPlotTablet
          v-if="tabletView"
          id="fc-true-false-svg"
        />
        <fckeyPlotMobile
          v-else-if="mobileView"
          id="fc-true-false-svg"
        />
        <fckeyPlotDesktop
          v-else
          id="fc-true-false-svg"
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
    <template #belowExplanation>
      <p v-html="text.paragraph3" />
    </template>
  </VizSection>
</template>

<script setup>
    import { onMounted } from "vue";
    import * as d3 from 'd3';
    import { isMobileOnly } from 'mobile-device-detect';
    import { isTablet } from 'mobile-device-detect';
    import VizSection from '@/components/VizSection.vue';
    import fckeyPlotDesktop from "@/assets/svgs/fc_tf_key_desktop.svg";
    import fckeyPlotTablet from "@/assets/svgs/fc_tf_key_tablet.svg";
    import fckeyPlotMobile from "@/assets/svgs/fc_tf_key_mobile.svg";

    // global variables
    const mobileView = isMobileOnly;
    const tabletView = isTablet;

    // define props
    const props = defineProps({
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
      addAriaLabel("#fc-true-false-svg");
      addInteractions();
    });
    
    function addAriaLabel(svgId) {
      const obsvSVG = d3.select(svgId)

      obsvSVG
        .attr("aria-label", props.text.ariaLabel)

      obsvSVG.selectChildren()
        .attr("aria-hidden", true)
    }

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
            // plot sankey
            draw_sankey(tf_id);
            // plot parent sankey
            if (tf_id.length > 2){
              draw_sankey(tf_id.slice(0,-3));
            }
        }
      else if (event.currentTarget.id.startsWith("tf-label-")){
            let tf_id = event.currentTarget.id.slice(9);
            // plot sankey
            draw_sankey(tf_id);
            // plot parent sankey
            if (tf_id.length > 2){
              draw_sankey(tf_id.slice(0,-3));
            }
        }
      else if (event.currentTarget.id.startsWith("tf-swoop-")){
            // plot sankey
            draw_sankey(tf_id);
            // plot parent sankey
            if (tf_id.length > 2){
              draw_sankey(tf_id.slice(0,-3));
            }
        }
      }

    function mouseout(event) {
      if (event.currentTarget.id.startsWith("tf-bar-")){
            let tf_id = event.currentTarget.id.slice(7);
            // remove sankey
            remove_sankey(tf_id);
            // remove parent sankey
            if (tf_id.length > 2){
              remove_sankey(tf_id.slice(0,-3));
            }
        }
      else if (event.currentTarget.id.startsWith("tf-label-")){
            let tf_id = event.currentTarget.id.slice(9);
            // remove sankey
            remove_sankey(tf_id);
            // remove parent sankey
            if (tf_id.length > 2){
              remove_sankey(tf_id.slice(0,-3));
            }
        }
      else if (event.currentTarget.id.startsWith("tf-swoop-")){
            let tf_id = event.currentTarget.id.slice(9);
            // remove sankey
            remove_sankey(tf_id);
            // remove parent sankey
            if (tf_id.length > 2){
              remove_sankey(tf_id.slice(0,-3));
            }
        }
      }


    function mouseleave(default_swoop) {
        draw_sankey(default_swoop);
    }

    function mouseenter(default_swoop) {
        remove_sankey(default_swoop);
    }

    function addInteractions() {
        // set viewbox for svg with confidence interval chart
        const fckeySVG = d3.select("#fc-true-false-svg")

        // plot parameters
        const default_swoop = "ND"

        draw_sankey(default_swoop);
        // Add interaction to confidence interval chart
        fckeySVG.select("#figure-forecast_truefalse_key")
            .on("mouseleave", () => mouseleave(default_swoop))
            .on("mouseenter", () => mouseenter(default_swoop));
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
        margin: 2rem auto 1.5rem auto;
        grid-template-areas:
            "chart";
    }
    #fc-true-false-svg {
        grid-area: chart;
        place-self: center;
        height: 100%;
        width: 100%;
    }
</style>
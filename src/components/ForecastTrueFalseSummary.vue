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
          :aria-label="text.ariaLabel"
        />
        <fcsumTFPlotMobile
          v-else-if="mobileView"
          id="fc-true-false-sum-svg"
          :aria-label="text.ariaLabel"
        />
        <fcsumTFPlotDesktop
          v-else
          id="fc-true-false-sum-svg"
          :aria-label="text.ariaLabel"
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
      hideSVGChildren("#fc-true-false-sum-svg");
    });

    function hideSVGChildren(svgId) {
      d3.select(svgId).selectChildren()
        .attr("aria-hidden", true)
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
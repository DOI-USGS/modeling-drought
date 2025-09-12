<template>
  <VizSection
    id="loss-function"
    :figures="true"
    :fig-caption="true"
  >
    <!-- HEADING -->
    <template #heading>
      <h3>
        {{ text.heading }}
      </h3>
    </template>
    <!-- FIGURES -->
    <template #aboveExplanation>
      <p v-html="text.paragraph1" />
    </template>
    <template #figures>
      <div id="lf-diagram-grid-container">
        <lfDiagramTablet
          v-if="tabletView"
          role="img"
          :id="svgId"
          :aria-label="text.ariaLabelResponsive"
        />
        <lfDiagramMobile
          v-else-if="mobileView"
          role="img"
          :id="svgId"
          :aria-label="text.ariaLabelResponsive"
        />
        <lfDiagramDesktop
          v-else
          role="img"
          :id="svgId"
          :aria-label="text.ariaLabelDesktop"
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
  import lfDiagramDesktop from "@/assets/svgs/lf_diagram_desktop.svg";
  import lfDiagramTablet from "@/assets/svgs/lf_diagram_tablet.svg";
  import lfDiagramMobile from "@/assets/svgs/lf_diagram_mobile.svg";

  // global variables
  const mobileView = isMobileOnly;
  const tabletView = isTablet;
  const svgId = "lf-diagram-svg"

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
    hideSVGChildren(svgId);
    addSVGDesc(svgId);
  });

  function hideSVGChildren(svgId) {
    d3.select(`#${svgId}`).selectChildren()
      .attr("aria-hidden", true)
  }

  function addSVGDesc(svgId) {
    if (mobileView | tabletView) {
      d3.select(`#${svgId}`).append('desc')
        .attr("id", `${svgId}-desc`)
        .text(props.text.ariaDescResponsive)
    } else {
      d3.select(`#${svgId}`).append('desc')
        .attr("id", `${svgId}-desc`)
        .text(props.text.ariaDescDesktop)
    }
  }
</script>

<style scoped lang="scss">
  #lf-diagram-grid-container {
    display: grid;
    width: 100%;
    max-width: 1200px;
    margin: 3rem auto 2rem auto;
    grid-template-areas:
      "chart";
  }
  #lf-diagram-svg {
    grid-area: chart;
    place-self: center;
    height: 100%;
    width: 100%;
  }
</style>
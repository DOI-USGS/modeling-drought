<template>
  <VizSection
    id="forecast-timeseries"
    :figures="true"
    :fig-caption="true"
  >
    <template #aboveExplanation>
      <p>
        <span v-html="text.paragraph1Start" />
        <button
          id="scroll-button"
          type="button"
          aria-label="Scroll to section on how the model captures uncertainty"
          @click="scrollToUncertainty"
        >
          <a v-html="text.paragraph1Button" />
        </button>
        <span v-html="text.paragraph1End" />
      </p>
    </template>
    <template #figures>
      <div id="fc-diagram-grid-container">
        <fcDiagramPlot
          role="img"
          :id="svgId"
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
  import VizSection from '@/components/VizSection.vue';
  import fcDiagramPlot from "@/assets/svgs/fc_diagram.svg";


  // define props
  const props = defineProps({
    text: { 
      type: Object,
        default() {
          return {}
        } 
    }
  })

  // global variables
  const svgId = "fc-diagram-svg"

  onMounted(() => {
    hideSVGChildren(svgId);
  });

  function hideSVGChildren(svgId) {
    d3.select(`#${svgId}`).selectChildren()
      .attr("aria-hidden", true)
  }
</script>

<style scoped lang="scss">
    #fc-diagram-grid-container {
        display: grid;
        width: 100%;
        max-width: 400px;
        margin: 2rem auto 2rem auto;
        grid-template-areas:
            "chart";
    }
    #fc-diagram-svg {
        grid-area: chart;
        place-self: center;
        height: 100%;
        width: 100%;
    }
    #scroll-button {
      background-color: transparent;
      border: none;
      padding: 0;
    }
</style>
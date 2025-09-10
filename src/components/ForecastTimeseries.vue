<template>
  <VizSection
    id="forecast-timeseries"
    :figures="true"
    :fig-caption="true"
  >
    <template #aboveExplanation>
      <p v-html="text.paragraph1" />
    </template>
    <template #figures>
      <div id="fc-diagram-grid-container">
        <fcDiagramPlot
          id="fc-diagram-svg"
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
  import VizSection from '@/components/VizSection.vue';
  import fcDiagramPlot from "@/assets/svgs/fc_diagram.svg";


  // define props
  defineProps({
    text: { 
      type: Object,
        default() {
          return {}
        } 
    }
  })

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
</style>
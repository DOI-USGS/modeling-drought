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
    <template #belowExplanation>
      <CollapsibleAccordion 
        v-for="item, index in text.accordionData"
        :key="index"
        :heading="item.heading"
        :content="item.content"
        :active-on-load="item.activeOnLoad"
        left-border-color="var(--usgs-blue_3_1)"
        button-active-background-color="var(--extremely-faded-usgs-blue)"
        button-inactive-background-color="var(--color-background)"
        button-font-weight="300"
        button-font-color="var(--color-title-text)"
      />
    </template>
  </VizSection>
</template>

<script setup>
  import VizSection from '@/components/VizSection.vue';
  import CollapsibleAccordion from '@/components/CollapsibleAccordion.vue';
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

  function getImageURL(file) {
    return new URL(`../assets/images/${file}`, import.meta.url).href
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
</style>
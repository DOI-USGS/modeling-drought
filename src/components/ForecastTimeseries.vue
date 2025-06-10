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
      <div
        class="timeseries-image-container"
      >
        <img
          :src="getImageURL(text.figure)"
          class="timeseries-image"
        >
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
.timeseries-image-container {
  text-align: center;
  margin-top: 2rem;
}
.timeseries-image {
  padding: 10px;
  max-width: 70rem;
}
</style>
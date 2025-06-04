<template>
  <VizSection
    id="forecast-timeseries"
    :figures="true"
    :fig-caption="true"
  >
    <template #aboveExplanation>
      <p v-html="text.paragraph1" />
      <p v-html="text.paragraph2" />
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
  </VizSection>
</template>

<script setup>
  import VizSection from '@/components/VizSection.vue';

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
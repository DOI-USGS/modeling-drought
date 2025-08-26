<template>
  <VizSection
    id="mapper-diagram"
    :figures="true"
    :fig-caption="true"
  >
    <template #aboveExplanation>
      <p v-html="text.paragraph1" />
    </template>
    <template #figures>
      <div id="mapper-image-container">
        <img
          :src="getImageURL(text.figurePath)"
          class="mapper-image"
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

<style scoped>
.mapper-image-container {
  text-align: center;
}
.mapper-image {
  padding: 10px;
  max-width: 95%;
}
</style>
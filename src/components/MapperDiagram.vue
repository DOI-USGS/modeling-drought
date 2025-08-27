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
          v-if="!mobileView"
          :src="getImageURL(text.mapPathDesktop)"
          class="mapper-image"
        >
        <img
          v-if="mobileView"
          :src="getImageURL(text.mapPathMobile)"
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
  import { isMobileOnly } from 'mobile-device-detect';
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

  // global variables
  const mobileView = isMobileOnly;

  function getImageURL(file) {
    return new URL(`../assets/images/${file}`, import.meta.url).href
  }
</script>

<style scoped>
#mapper-image-container {
  display: flex;
  justify-items: center;
  flex-direction: column;
  gap: 3rem;
  margin: 0 auto 0 auto;
  @media only screen and (max-width: 600px) {
    max-width: 90vw; /* 90% of view width on mobile */
  }
}
.mapper-image {
  padding: 10px;
  max-width: 100%;
  margin: 0 auto 0 auto;
}
</style>
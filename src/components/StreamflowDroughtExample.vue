<template>
  <VizSection
    id="river-diagram"
    :figures="true"
    :fig-caption="true"
  >
    <template #figures>
      <div
        class="river-image-container"
      >
        <img
          :src="getImageURL(text.figurePath)"
          class="river-image"
          :alt="text.figureAlt"
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
#river-image-container {
  display: flex;
  justify-items: center;
  flex-direction: column;
  gap: 3rem;
  margin: 0 auto 0 auto;
  @media only screen and (max-width: 600px) {
    max-width: 90vw; /* 90% of view width on mobile */
  }
}
.river-image {
  padding: 10px;
  max-width: 100%;
  margin: 0 auto 0 auto;
}
</style>
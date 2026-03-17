<template>
  <section>
    <div
      class="text-container"
    >
      <h3 v-html="text.heading" />
      <div
        id="define-low-streamflow-accordion-container"
      >
        <CollapsibleAccordion 
          v-for="item, index in text.classifyStreamflowAccordionData"
          :key="index"
          accordion-id="define-low-streamflow-accordion"
          :heading="item.heading"
          :content="item.content"
          :active-on-load="item.activeOnLoad"
          left-border-color="var(--usgs-blue_3_1)"
          button-active-background-color="var(--extremely-faded-usgs-blue)"
          button-inactive-background-color="var(--color-background)"
          button-font-weight="300"
          button-font-color="var(--color-title-text)"
        />
      </div>
      <p v-html="text.paragraph1" />
      <div
        class="explainer-image-container"
      >
        <img
          :src="getImageURL(text.figurePath)"
          class="explainer-image"
          :alt="text.figureAlt"
        >
      </div>
      <p v-html="text.paragraph2" />
    </div>
  </section>
</template>

<script setup>
  import CollapsibleAccordion from "@/components/CollapsibleAccordion.vue";

  // define props
  defineProps({
    text: {  
      type: Object,
      default: () => ({})
    }
  })

  function getImageURL(file) {
    return new URL(`../assets/images/${file}`, import.meta.url).href
  }
</script>

<style scoped>
#define-low-streamflow-accordion-container {
  margin-bottom: 20px;
}
.explainer-image-container {
  text-align: center;
}
.explainer-image {
  padding: 10px;
  max-width: 95%;
}
</style>
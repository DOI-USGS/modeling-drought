<template>
  <section>
    <div
      class="text-container"
    >
      <h2
        class="section-title"
      >
        <span>
          {{ text.title }}
        </span>
      </h2>
      <p
        class="section-subtitle"
        v-html="text.subtitle"
      />
      <p v-html="text.paragraph1" />
      <p v-html="text.paragraph2" />
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
</script>

<style>
</style>
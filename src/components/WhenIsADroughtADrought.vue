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
      <DefineLowStreamflow
        :text="text.defineLowStreamflow"
      />
      <ClassifyStreamflowDrought
        :text="text.classifyStreamflowDrought"
      />
      <CollapsibleAccordion 
        v-for="item, index in text.accordionData"
        accordion-id="low-flow-accordion"
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
  import DefineLowStreamflow from "@/components/DefineLowStreamflow.vue";
  import ClassifyStreamflowDrought from "@/components/ClassifyStreamflowDrought.vue";
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
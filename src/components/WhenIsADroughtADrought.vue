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
      <StreamflowDroughtExample
        :text="text.streamflowDroughtExample"
      />
      <DefineLowStreamflow
        :text="text.defineLowStreamflow"
      />
      <ClassifyStreamflowDrought
        :text="text.classifyStreamflowDrought"
      />
      <CollapsibleAccordion 
        v-for="item, index in text.accordionData"
        :key="index"
        accordion-id="low-flow-accordion"
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
  <ObservationExplore
    :text="text.observationExplore"
  />
</template>

<script setup>
  import StreamflowDroughtExample from "@/components/StreamflowDroughtExample.vue";
  import DefineLowStreamflow from "@/components/DefineLowStreamflow.vue";
  import ClassifyStreamflowDrought from "@/components/ClassifyStreamflowDrought.vue";
  import CollapsibleAccordion from "@/components/CollapsibleAccordion.vue";
  import ObservationExplore from '@/components/ObservationExplore.vue';

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
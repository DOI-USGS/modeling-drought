<template>
  <ForecastArt
  />
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
      <MapperDiagram
        :text="text.mapperDiagram"
      />
    </div>
  </section>
</template>

<script setup>
  import ForecastArt from '@/components/ForecastArt.vue';
  import MapperDiagram from '@/components/MapperDiagram.vue';

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
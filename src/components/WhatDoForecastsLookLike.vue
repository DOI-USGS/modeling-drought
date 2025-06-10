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
    </div>
    <ForecastTimeseries
      :text="text.forecastTimeseries"
    />
    <ForecastExplore
      :text="text.forecastExplore"
    />
  </section>
</template>

<script setup>
  import ForecastTimeseries from '@/components/ForecastTimeseries.vue';
  import ForecastExplore from '@/components/ForecastExplore.vue';

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
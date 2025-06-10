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
    <ForecastSummary 
      :text="text.forecastSummary"
    />
  </section>
</template>

<script setup>
  import ForecastSummary from '@/components/ForecastSummary.vue';

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
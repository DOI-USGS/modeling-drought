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
      <p v-html="text.paragraph3" />
    </div>
    <LossFunction
      :text="text.lossFunction"
    />
    <PredictionInterval
      :text="text.predictionInterval"
    />
  </section>
</template>

<script setup>
  import LossFunction from '@/components/LossFunction.vue';
  import PredictionInterval from '@/components/PredictionInterval.vue';

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
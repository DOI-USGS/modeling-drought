<template>
  <section>
    <div
      class="text-container"
    >
      <h2
        id="uncertainty-section-title"
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
    <LossFunctionDiagram
      :text="text.lossFunctionDiagram"
    />
    <LossFunction
      :text="text.lossFunction"
    />
    <PredictionInterval
      :text="text.predictionInterval"
    />
  </section>
</template>

<script setup>
  import LossFunctionDiagram from '@/components/LossFunctionDiagram.vue';
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
  .group-label.median {
    background-color: var(--color-median);
    color: white;
  }
  .group-label.q95 {
    background-color: var(--color-quantile-95);
    color: white;
  }
  .group-label.q5 {
    background-color: var(--color-quantile-5);
  }
</style>
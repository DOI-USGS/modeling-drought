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
    <ForecastTrueFalseSankey
      :text="text.forecastTrueFalseSankey"
    />
    <ForecastTrueFalseSummary
      :text="text.forecastTrueFalseSummary"
    />
    <ForecastTrueFalseRightOrWrong
      :text="text.forecastTrueFalseRightOrWrong"
    />
  </section>
</template>

<script setup>
  import ForecastTrueFalseSankey from '@/components/ForecastTrueFalseSankey.vue';
  import ForecastTrueFalseSummary from '@/components/ForecastTrueFalseSummary.vue';
  import ForecastTrueFalseRightOrWrong from '@/components/ForecastTrueFalseRightOrWrong.vue';

  // define props
  defineProps({
    text: {  
      type: Object,
      default: () => ({})
    }
  })
</script>

<style>
  .right {
    background-color: var(--grey_7_1);
    color: white;
  }
  .wrong {
    background-color: var(--grey_3_1);
  }
  .true-neg {
    background-color: var(--color-true-negative);
    color: white;
  }
  .false-neg {
    background-color: var(--color-false-negative);
  }
  .true-pos {
    background-color: var(--color-true-positive);
  }
  .false-pos {
    background-color: var(--color-false-positive);
  }
</style>
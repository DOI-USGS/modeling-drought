<template>
  <section id="visualization-container">
    <div
      class="text-container"
    >
      <h1 
        class="title" 
        v-html="text.pageTitle" 
      />
    </div>
    <div
      class="text-container"
    >
      <h2
        class="subtitle"
      >
        <span>
          {{ text.sections.A.title }}
        </span>
      </h2>
    </div>
    <LossFunction
      :text="text.components.LossFunction"
    />
    <PredictionInterval
      :text="text.components.PredictionInterval"
    />
    <div
      class="text-container"
    >
      <h2
        class="subtitle"
      >
        <span>
          {{ text.sections.B.title }}
        </span>
      </h2>
    </div>
    <ForecastConfidence
      :text="text.components.ForecastConfidence"
    />
    <ForecastSummary
      :text="text.components.ForecastSummary"
    />
    <ForecastTrueFalse
      :text="text.components.ForecastTrueFalse"
    />
    <div
      class="text-container"
    >
      <h2
        class="subtitle"
      >
        <span>
          {{ text.sections.C.title }}
        </span>
      </h2>
    </div>
    <div
      class="text-container"
    >
      <h2
        class="subtitle"
      >
        <span>
          {{ text.sections.D.title }}
        </span>
      </h2>
    </div>
    <AboutTheTeam
      :text="text.components.AboutTheTeam"
    />
    <div
      class="text-container"
    >
      <h2
        class="subtitle"
      >
        <span>
          {{ text.sections.references.title }}
        </span>
      </h2>
    </div>
    <ReferencesSection
      :references="references"
    />
    <div
      class="text-container"
    >
      <h2
        class="subtitle"
      >
        <span>
          {{ text.sections.authors.title }}
        </span>
      </h2>
    </div>
    <AuthorshipSection
      :authors="authors"
    />
  </section>
</template>

<script setup>
  // import { isMobile } from 'mobile-device-detect';

  import text from "@/assets/text/text.js";
  import references from "@/assets/text/references";
  import authors from "@/assets/text/authors";
  import ReferencesSection from '@/components/ReferencesSection.vue';
  import AuthorshipSection from '@/components/AuthorshipSection.vue';
  import LossFunction from '@/components/LossFunction.vue';
  import PredictionInterval from '@/components/PredictionInterval.vue';
  import ForecastConfidence from '@/components/ForecastConfidence.vue';
  import ForecastSummary from '@/components/ForecastSummary.vue';
  import ForecastTrueFalse from '@/components/ForecastTrueFalse.vue';
  import AboutTheTeam from '@/components/AboutTheTeam.vue';

  // global variables
  // const mobileView = isMobile;
</script>

<style scoped>
.title {
  font-family: sans-serif; /* This is fallback font for old browsers */
  font-family: var(--title-font);
} 
.subtitle {
  font-family: sans-serif; /* This is fallback font for old browsers */
  font-family: var(--subtitle-font);
  width: 100%;
  text-align:left; 
  border-bottom: 1px solid var(--color-lowlight); 
  overflow: inherit;
}
.subtitle span {
  position: relative;
  top: 1rem;
}
</style>
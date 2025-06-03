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
    <WhatIsStreamflowDrought 
      :text="text.sections.WhatIsStreamflowDrought"
    />
    <HowModelStreamflowDrought 
      :text="text.sections.HowModelStreamflowDrought"
    />
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
        class="section-title"
      >
        <span>
          {{ text.sections.C.title }}
        </span>
      </h2>
    </div>
    <ForecastConfidence
      :text="text.components.ForecastConfidence"
    />
    <ForecastSummary
      :text="text.components.ForecastSummary"
    />
    <div
      class="text-container"
    >
      <h2
        class="section-title"
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
        class="section-title"
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
        class="section-title"
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
        class="section-title"
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
  import AboutTheTeam from '@/components/AboutTheTeam.vue';
  import WhatIsStreamflowDrought from "@/components/WhatIsStreamflowDrought.vue";
  import HowModelStreamflowDrought from "@/components/HowModelStreamflowDrought.vue";

  // global variables
  // const mobileView = isMobile;

</script>

<style scoped>
</style>
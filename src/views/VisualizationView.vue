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
        class="section-title"
      >
        <span>
          {{ text.sections.A.title }}
        </span>
      </h2>
      <p
        class="section-subtitle"
      >
        {{ text.sections.A.subtitle }}
      </p>
      <p v-html="text.sections.A.paragraph1" />
      <p v-html="text.sections.A.paragraph2" />
      <CollapsibleAccordion 
        v-for="item, index in text.sections.A.accordionData"
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
  import CollapsibleAccordion from "@/components/CollapsibleAccordion.vue";
  import ReferencesSection from '@/components/ReferencesSection.vue';
  import AuthorshipSection from '@/components/AuthorshipSection.vue';
  import LossFunction from '@/components/LossFunction.vue';
  import PredictionInterval from '@/components/PredictionInterval.vue';
  import ForecastConfidence from '@/components/ForecastConfidence.vue';
  import ForecastSummary from '@/components/ForecastSummary.vue';
  import AboutTheTeam from '@/components/AboutTheTeam.vue';

  // global variables
  // const mobileView = isMobile;

</script>

<style scoped>
.title {
  font-family: sans-serif; /* This is fallback font for old browsers */
  font-family: var(--title-font);
} 
.section-title {
  font-family: sans-serif; /* This is fallback font for old browsers */
  font-family: var(--title-font);
  width: 100%;
  text-align:left; 
  border-bottom: 1px solid var(--color-lowlight); 
  overflow: inherit;
}
.section-title span {
  position: relative;
  top: 1rem;
}
.section-subtitle {
  color: var(--color-subtitle-text);
  font-weight: 300;
  margin-bottom: 3rem;
}
</style>
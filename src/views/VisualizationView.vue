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
    <WhatDoForecastsLookLike 
      :text="text.sections.WhatDoForecastsLookLike"
    />
    <HowWellModelPerform 
      :text="text.sections.HowWellModelPerform"
    />
    <HowCaptureUncertainty 
      :text="text.sections.HowCaptureUncertainty"
    />
    <ForecastSummary
      :text="text.components.ForecastSummary"
    />
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
  import ForecastSummary from '@/components/ForecastSummary.vue';
  import AboutTheTeam from '@/components/AboutTheTeam.vue';
  import WhatIsStreamflowDrought from "@/components/WhatIsStreamflowDrought.vue";
  import HowModelStreamflowDrought from "@/components/HowModelStreamflowDrought.vue";
  import WhatDoForecastsLookLike from "@/components/WhatDoForecastsLookLike.vue";
  import HowWellModelPerform from "@/components/HowWellModelPerform.vue"
  import HowCaptureUncertainty from "@/components/HowCaptureUncertainty.vue"

  // global variables
  // const mobileView = isMobile;

</script>

<style scoped>
</style>
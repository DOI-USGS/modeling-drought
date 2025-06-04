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
      :text="text.WhatIsStreamflowDrought"
    />
    <HowModelStreamflowDrought 
      :text="text.HowModelStreamflowDrought"
    />
    <WhatDoForecastsLookLike 
      :text="text.WhatDoForecastsLookLike"
    />
    <HowWellModelPerform 
      :text="text.HowWellModelPerform"
    />
    <HowCaptureUncertainty 
      :text="text.HowCaptureUncertainty"
    />
    <HowUncertaintyChange 
      :text="text.HowUncertaintyChange"
    />
    <WhatsNext 
      :text="text.WhatsNext"
    />
    <WhoContributing 
      :text="text.WhoContributing"
    />
    <div
      class="text-container"
    >
      <h2
        class="section-title"
      >
        <span>
          {{ text.References.title }}
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
          {{ text.Authors.title }}
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
  import WhatIsStreamflowDrought from "@/components/WhatIsStreamflowDrought.vue";
  import HowModelStreamflowDrought from "@/components/HowModelStreamflowDrought.vue";
  import WhatDoForecastsLookLike from "@/components/WhatDoForecastsLookLike.vue";
  import HowWellModelPerform from "@/components/HowWellModelPerform.vue"
  import HowCaptureUncertainty from "@/components/HowCaptureUncertainty.vue"
  import HowUncertaintyChange from "@/components/HowUncertaintyChange.vue"
  import WhatsNext from "@/components/WhatsNext.vue";
  import WhoContributing from "@/components/WhoContributing.vue";
  import ReferencesSection from '@/components/ReferencesSection.vue';
  import AuthorshipSection from '@/components/AuthorshipSection.vue';

  // global variables
  // const mobileView = isMobile;

</script>

<style scoped>
</style>
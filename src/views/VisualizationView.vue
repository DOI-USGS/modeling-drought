<template>
  <section id="visualization-container">
    <div class="text-container" :class="{ mobile: mobileView}">
      <h1 class = 'title'>
        {{ text.pageTitle }}
      </h1>
    </div>
    <IntroSection
      :text="text.components.IntroSection"
    />
    <SectionTitle
      :content="text.sections.A"
      :height=sectionTitleHeight
      :overlay=true
      :overlayOpacity=sectionTitleOverlayOpacity
    />
      <LossFunction
        :text="text.components.LossFunction"
      />
      <ConfidenceInterval
        :text="text.components.ConfidenceInterval"
      />
    <SectionTitle
      :content="text.sections.B"
      :height=sectionTitleHeight
      :overlay=true
      :overlayOpacity=sectionTitleOverlayOpacity
    />
      <Forecast
        :text="text.components.Forecast"
      />
    <!-- Put component(s) here. Use VizSection template inside component (as in Introsection.Vue, RegionalViolins.vue, BarChartExample.vue)-->
    <SectionTitle
      :content="text.sections.C"
      :height=sectionTitleHeight
      :overlay=true
      :overlayOpacity=sectionTitleOverlayOpacity
    />
    <!-- Put component(s) here. Use VizSection template inside component (as in Introsection.Vue, RegionalViolins.vue, BarChartExample.vue)-->
    <SectionTitle
      :content="text.sections.D"
      :height=sectionTitleHeight
      :overlay=true
      :overlayOpacity=sectionTitleOverlayOpacity
    />
    <AboutTheTeam
        :text="text.components.AboutTheTeam"
      />
    <ReferencesSection />
    <AuthorshipSection titleLevel="2" :authors="authors"/>
  </section>
</template>

<script setup>
  import { isMobile } from 'mobile-device-detect';

  import text from "@/assets/text/text.js";
  import authors from "@/assets/text/authors";
  import IntroSection from '@/components/IntroSection.vue'
  import SectionTitle from '@/components/SectionTitle.vue';
  import ReferencesSection from '@/components/ReferencesSection.vue';
  import AuthorshipSection from '@/components/AuthorshipSection.vue';
  import LossFunction from '@/components/LossFunction.vue';
  import ConfidenceInterval from '@/components/ConfidenceInterval.vue';
  import Forecast from '@/components/Forecast.vue';
  import AboutTheTeam from '@/components/AboutTheTeam.vue';


  // global variables
  const mobileView = isMobile;
  const sectionTitleHeight = mobileView ? 25 : 50;
  const sectionTitleOverlayOpacity = 0.7;
</script>

<style scoped>
</style>
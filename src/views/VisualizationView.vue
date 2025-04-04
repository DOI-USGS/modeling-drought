<template>
  <section id="visualization-container">
    <div
      class="text-container"
      :class="{ mobile: mobileView}"
    >
      <h1 class="title">
        {{ text.pageTitle }}
      </h1>
    </div>
    <SectionTitle
      :content="text.sections.A"
      :height="sectionTitleHeight"
      :overlay="true"
      :overlay-opacity="sectionTitleOverlayOpacity"
    />
    <LossFunction
      :text="text.components.LossFunction"
    />
    <PredictionInterval
      :text="text.components.PredictionInterval"
    />
    <SectionTitle
      :content="text.sections.B"
      :height="sectionTitleHeight"
      :overlay="true"
      :overlay-opacity="sectionTitleOverlayOpacity"
    />
    <ForecastConfidence
      :text="text.components.Forecast"
    />
    <SectionTitle
      :content="text.sections.C"
      :height="sectionTitleHeight"
      :overlay="true"
      :overlay-opacity="sectionTitleOverlayOpacity"
    />
    <SectionTitle
      :content="text.sections.D"
      :height="sectionTitleHeight"
      :overlay="true"
      :overlay-opacity="sectionTitleOverlayOpacity"
    />
    <AboutTheTeam
      :text="text.components.AboutTheTeam"
    />
    <ReferencesSection
      title-level="2"
      :references="references"
    />
    <AuthorshipSection
      title-level="2"
      :authors="authors"
    />
  </section>
</template>

<script setup>
  import { isMobile } from 'mobile-device-detect';

  import text from "@/assets/text/text.js";
  import references from "@/assets/text/references";
  import authors from "@/assets/text/authors";
  import SectionTitle from '@/components/SectionTitle.vue';
  import ReferencesSection from '@/components/ReferencesSection.vue';
  import AuthorshipSection from '@/components/AuthorshipSection.vue';
  import LossFunction from '@/components/LossFunction.vue';
  import PredictionInterval from '@/components/PredictionInterval.vue';
  import ForecastConfidence from '@/components/ForecastConfidence.vue';
  import AboutTheTeam from '@/components/AboutTheTeam.vue';


  // global variables
  const mobileView = isMobile;
  const sectionTitleHeight = mobileView ? 25 : 50;
  const sectionTitleOverlayOpacity = 0.7;
</script>

<style scoped>
</style>
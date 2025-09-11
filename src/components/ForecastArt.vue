<template>
  <VizSection
    id="forecast-art"
    :figures="true"
    :fig-caption="true"
  >
    <template #figures>
      <div id="fc-art-grid-container">
        <fcArtPlot
          id="fc-art-svg"
        />
      </div>
    </template>
  </VizSection>
</template>

<script setup>
    import VizSection from '@/components/VizSection.vue';
    import fcArtPlot from "@/assets/svgs/fc_art_desktop.svg";


    // define props
    defineProps({
        text: { 
        type: Object,
            default() {
            return {}
            } 
        }
    })

</script>

<style scoped lang="scss">
    #fc-art-grid-container {
        display: grid;
        width: 100%;
        max-width: 600px;
        margin: 2rem auto 2rem auto;
        grid-template-areas:
            "chart";
    }
    #fc-art-svg {
        grid-area: chart;
        place-self: center;
        height: 100%;
        width: 100%;
    }
</style>
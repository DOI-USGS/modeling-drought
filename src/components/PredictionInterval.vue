<template>
  <VizSection
    id="confidence-interval"
    :figures="true"
    :fig-caption="true"
  >
    <!-- HEADING -->
    <template #heading>
      <h3>
        {{ text.heading }}
      </h3>
    </template>
    <!-- FIGURES -->
    <template #aboveExplanation>
      <p v-html="text.paragraph1" />
      <RadioGroup
        v-model="selectedLayer"
        :options="layers"
        :center-color="centerColor"
      />
    </template>
    <template #figures>
      <div id="pi-grid-container">
        <piPlotMobile
          v-if="mobileView"
          id="pi-svg"
        />
        <piPlotDesktop
          v-else
          id="pi-svg"
        />
      </div>
    </template>
    <!-- FIGURE CAPTION -->
    <template #figureCaption>
      <p v-html="text.caption" />
    </template>
  </VizSection>
</template>

<script setup>
    import { onMounted, reactive, ref, watch } from "vue";
    import * as d3 from 'd3';
    import { isMobile } from 'mobile-device-detect';
    import VizSection from '@/components/VizSection.vue';
    import RadioGroup from '@/components/RadioGroup.vue'
    import piPlotDesktop from "@/assets/svgs/pi_example_desktop.svg";
    import piPlotMobile from "@/assets/svgs/pi_example_mobile.svg";

    // global variables
    const mobileView = isMobile;

    // define props
    defineProps({
        text: { 
            type: Object,
            default() {
                return {}
            } 
        }
    })

    // define reactive variables
    const selectedLayer = ref('MEDIAN')
    const layers = reactive([
        {
            label: 'Median',
            value: 'MEDIAN',
            color: '#00264c'
        },
        {
            label: '50% prediction interval',
            value: '2',
            color: '#929292'
        },
        {
            label: '75% prediction interval',
            value: '1',
            color: '#929292'
        },
        {
            label: '90% prediction interval',
            value: '0',
            color: '#929292'
        }
    ])

    // define global variables
    const centerColor = 'var(--color-background)'

    // Watches selectedLayer for changes and updates figure layers
    watch(selectedLayer, () => {
        updateFigure()
    })

    // Declare behavior on mounted
    // functions called here
    onMounted(() => {
        // FOR NOW, drop button annotations (won't exist in futurre)
        // hide annotations
        d3.select("#annotation_buttons2").selectAll("text")
            .style("opacity", 0);
        for(let i=1;i<=4;i++){
            d3.select("#annotation_buttons2_arrow"+i.toString()).selectAll("path")
                .style("opacity", 0);
        }
        // update figure based on radio button selection
        updateFigure();
    });

    function updateFigure() {
        layers.map(layer => {
            const targetOpacity = layer.value === selectedLayer.value ? 1 : 0;
            toggleLayer(layer.value, targetOpacity)
        })
        const legendOpacity = selectedLayer.value == 'MEDIAN' ? 0 : 1;
        toggleLegend(legendOpacity)
    }

    function toggleLayer(targetID, targetOpacity) {
        d3.select("#TAG-" + targetID + "-LABEL-BOLD").selectAll("text")
            .style("opacity", targetOpacity);
        d3.select("#PI-PATCH-" + targetID).selectAll("path")
            .style("fill-opacity", targetOpacity * 0.5)
            .style("stroke-opacity", targetOpacity);
        if (targetID != "MEDIAN"){
            d3.select("#PI-PATCH-LOWER-" + targetID).selectAll("path")
                .style("stroke-opacity", targetOpacity);
            d3.select("#PI-PATCH-UPPER-" + targetID).selectAll("path")
                .style("stroke-opacity", targetOpacity);
            d3.select("#LF-LOWER-" + targetID).selectAll("path")
                .style("stroke-opacity", targetOpacity);
            d3.select("#LF-UPPER-" + targetID).selectAll("path")
                .style("stroke-opacity", targetOpacity);
            let hrefval = d3.select("#PI-missed-" + targetID + " use").attr("xlink:href")
            d3.select("#PI-missed-" + targetID).select(hrefval)
                .style("stroke-opacity", targetOpacity);
        }
    }

    function toggleLegend(targetOpacity) {
        d3.select("#legend-pi-missed").selectAll("use")
            .style("stroke-opacity", targetOpacity);
        d3.select("#legend-pi-missed").selectAll("text")
            .style("opacity", targetOpacity);
    }
</script>

<style scoped lang="scss">
    #pi-grid-container {
        display: grid;
        width: 100%;
        max-width: 1200px;
        margin: 3rem auto 4rem auto;
        grid-template-areas:
            "chart";
    }
    #pi-svg {
        grid-area: chart;
        place-self: center;
        height: 100%;
        width: 100%;
    }
</style>
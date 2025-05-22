<template>
  <VizSection
    id="forecast-true-false"
    :figures="true"
    :fig-caption="true"
  >
    <!-- HEADING -->
    <template #heading>
      <h3>
        {{ text.heading }}
      </h3>
    </template>
    <template #aboveExplanation>
      <p v-html="text.paragraph1" />
      <RadioGroup2
        v-model="selectedfcSumLayer"
        :options="fcSumLayers"
        :center-color="centerColorfcSum"
      />
    </template>
    <!-- FIGURES -->
    <template #figures>
      <div id="fc-true-false-sum-grid-container">
        <component :is="currentPlot" id="fc-true-false-sum-svg" />
      </div>
    </template>
    <!-- FIGURE CAPTION -->
    <template #figureCaption>
      <p v-html="text.caption" />
    </template>
  </VizSection>
</template>

<script setup>
    import { onMounted, reactive, ref, watch  } from "vue";
    import * as d3 from 'd3';
    import { isMobile } from 'mobile-device-detect';
    import { isTablet } from 'mobile-device-detect';
    import VizSection from '@/components/VizSection.vue';
    import RadioGroup2 from '@/components/RadioGroup.vue'
    import fcsumNDPlotDesktop from "@/assets/svgs/fc_tf_sum_nd_desktop.svg";
    import fcsumRWPlotDesktop from "@/assets/svgs/fc_tf_sum_rw_desktop.svg";
    import fcsumYDPlotDesktop from "@/assets/svgs/fc_tf_sum_yd_desktop.svg";
    import fcsumNDPlotTablet from "@/assets/svgs/fc_tf_sum_nd_tablet.svg";
    import fcsumRWPlotTablet from "@/assets/svgs/fc_tf_sum_rw_tablet.svg";
    import fcsumYDPlotTablet from "@/assets/svgs/fc_tf_sum_yd_tablet.svg";
    import fcsumNDPlotMobile from "@/assets/svgs/fc_tf_sum_nd_mobile.svg";
    import fcsumRWPlotMobile from "@/assets/svgs/fc_tf_sum_rw_mobile.svg";
    import fcsumYDPlotMobile from "@/assets/svgs/fc_tf_sum_yd_mobile.svg";

    // global variables
    const mobileView = isMobile;
    const tabletView = isTablet;

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
    const selectedfcSumLayer = ref('RW-all')
    const fcSumLayers = reactive([
        {
            label: 'how often is the model right or wrong?',
            value: 'RW-all',
            color: '#929292'
        },
        {
            label: 'how often is the model right of wrong when it does not predict drought?',
            value: 'RW_noDrought',
            color: '#406992'
        },
        {
            label: 'how often is the model right of wrong when it predicts drought?',
            value: 'RW-drought',
            color: '#B78935'
        }
    ])

    // define global variables
    const centerColorfcSum = 'var(--color-background)'
    const currentPlot = ref('');

    // Watches selectedLayer for changes and updates figure layers
    watch(selectedfcSumLayer, () => {
        updateFigure()
    })

    // Declare behavior on mounted
    // functions called here
    onMounted(() => {
        addInteractions();
        // update figure based on radio button selection
        updateFigure();
    });

    // Function to update the figure based on selected layer and device type
    function updateFigure() {
        if (tabletView) {
            switch (selectedfcSumLayer.value) {
                case 'RW_noDrought':
                    currentPlot.value = fcsumNDPlotTablet; // Change to the appropriate component for RW_noDrought
                    break;
                case 'RW-all':
                    currentPlot.value = fcsumRWPlotTablet; // Change to the appropriate component for RW-all
                    break;
                case 'RW-drought':
                    currentPlot.value = fcsumYDPlotTablet; // Change to the appropriate component for RW-drought
                    break;
                default:
                    currentPlot.value = fcsumRWPlotTablet; // Fallback
            }
        } else if (mobileView) {
            switch (selectedfcSumLayer.value) {
                case 'RW_noDrought':
                    currentPlot.value = fcsumNDPlotMobile;
                    break;
                case 'RW-all':
                    currentPlot.value = fcsumRWPlotMobile;
                    break;
                case 'RW-drought':
                    currentPlot.value = fcsumYDPlotMobile;
                    break;
                default:
                    currentPlot.value = fcsumRWPlotMobile; // Fallback
            }
        } else {
            // For desktop view
            switch (selectedfcSumLayer.value) {
                case 'RW_noDrought':
                    currentPlot.value = fcsumNDPlotDesktop;
                    break;
                case 'RW-all':
                    currentPlot.value = fcsumRWPlotDesktop;
                    break;
                case 'RW-drought':
                    currentPlot.value = fcsumYDPlotDesktop;
                    break;
                default:
                    currentPlot.value = fcsumRWPlotDesktop; // Fallback
            }
        }
    }

    // Draw the percent width line and label
    function draw_sankey(tf_id) {
        d3.select("#tf-bar-" + tf_id).selectAll("path")
            .style("fill-opacity", 1)
        d3.select("#tf-swoop-" + tf_id).selectAll("path")
            .style("fill-opacity", 0.2)
        d3.select("#tf-label-" + tf_id).selectAll("text")
            .style("opacity", 1);
    }

    // Draw the percent width line and label
    function remove_sankey(tf_id) {
        d3.select("#tf-bar-" + tf_id).selectAll("path")
            .style("fill-opacity", 0.25)
        d3.select("#tf-swoop-" + tf_id).selectAll("path")
            .style("fill-opacity", 0.05)
        d3.select("#tf-label-" + tf_id).selectAll("text")
            .style("opacity", 0.0);
    }

    function mouseover(event) {
      if (event.currentTarget.id.startsWith("tf-bar-")){
            let tf_id = event.currentTarget.id.slice(7);
            draw_sankey(tf_id);
            if (tf_id.length > 2){
              draw_sankey(tf_id.slice(0,-3));
              console.log(tf_id)
            }
        }
      else if (event.currentTarget.id.startsWith("tf-label-")){
            let tf_id = event.currentTarget.id.slice(9);
            draw_sankey(tf_id);
            if (tf_id.length > 2){
              draw_sankey(tf_id.slice(0,-3));
            }
        }
      else if (event.currentTarget.id.startsWith("tf-swoop-")){
            let tf_id = event.currentTarget.id.slice(9);
            draw_sankey(tf_id);
            if (tf_id.length > 2){
              draw_sankey(tf_id.slice(0,-3));
            }
        }
      }

    function mouseout(event) {
      if (event.currentTarget.id.startsWith("tf-bar-")){
            let tf_id = event.currentTarget.id.slice(7);
            remove_sankey(tf_id);
            if (tf_id.length > 2){
              remove_sankey(tf_id.slice(0,-3));
            }
        }
      else if (event.currentTarget.id.startsWith("tf-label-")){
            let tf_id = event.currentTarget.id.slice(9);
            remove_sankey(tf_id);
            if (tf_id.length > 2){
              remove_sankey(tf_id.slice(0,-3));
            }
        }
      else if (event.currentTarget.id.startsWith("tf-swoop-")){
            let tf_id = event.currentTarget.id.slice(9);
            remove_sankey(tf_id);
            if (tf_id.length > 2){
              remove_sankey(tf_id.slice(0,-3));
            }
        }
      }

    function addInteractions() {
        // set viewbox for svg with confidence interval chart
        const fckeySVG = d3.select("#fc-true-false-svg")
        // Add interaction to confidence interval chart
        fckeySVG.selectAll("g")
            .on("mouseover", (event) => mouseover(event))
            .on("mouseout", (event) => mouseout(event))
    }
</script>

<style scoped lang="scss">
    #fc-true-false-sum-grid-container {
        display: grid;
        width: 100%;
        max-width: 800px;
        margin: 3rem auto 4rem auto;
        grid-template-areas:
            "chart";
    }
    #fc-true-false-sum-svg {
        grid-area: chart;
        place-self: center;
        height: 100%;
        width: 100%;
    }
</style>
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
      <RadioGroup
        v-model="selectedfcSumLayer"
        radio-group-name="tf-radio-group"
        :options="fcSumLayers"
        :center-color="centerColorfcSum"
      />
    </template>
    <!-- FIGURES -->
    <template #figures>
      <div id="fc-true-false-rw-grid-container">
        <component
          :is="getCurrentSVG()"
          id="fc-true-false-rw-svg"
          :aria-label="ariaLabel"
        />
      </div>
    </template>
    <!-- FIGURE CAPTION -->
    <template #figureCaption>
      <p v-html="text.caption" />
    </template>
    <template #belowExplanation>
      <p v-html="text.paragraph2" />
    </template>
  </VizSection>
</template>

<script setup>
    import { computed, nextTick, onMounted, reactive, ref, watch  } from "vue";
    import * as d3 from 'd3';
    import { isMobileOnly } from 'mobile-device-detect';
    import { isTablet } from 'mobile-device-detect';
    import VizSection from '@/components/VizSection.vue';
    import RadioGroup from '@/components/RadioGroup.vue'
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
    const mobileView = isMobileOnly;
    const tabletView = isTablet;

    // define props
    const props = defineProps({
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
            label: props.text.questionAll,
            ariaLabel: props.text.questionAllAriaLabel,
            value: 'RW-all',
            color: 'var(--grey_3_1)'
        },
        {
            label: props.text.questionNoDrought,
            ariaLabel: props.text.questionNoDroughtAriaLabel,
            value: 'RW_noDrought',
            color: 'var(--color-true-negative)'
        },
        {
            label: props.text.questionDrought,
            ariaLabel: props.text.questionDroughtAriaLabel,
            value: 'RW-drought',
            color: 'var(--color-true-positive)'
        }
    ])
    const ariaLabel = computed(() => {
      let svgAriaLabel;
      switch(true) {
        case selectedfcSumLayer.value  == 'RW_noDrought':
          svgAriaLabel = props.text.rwNoDroughtAriaLabel;
          break;
        case selectedfcSumLayer.value  == 'RW-all':
          svgAriaLabel = props.text.rwAllAriaLabel;
          break;
        case selectedfcSumLayer.value  == 'RW-drought':
          svgAriaLabel = props.text.rwDroughtAriaLabel;
          break;
      }
      return svgAriaLabel;
    })

    // define global variables
    const centerColorfcSum = 'var(--color-background)'

    // Hide SVG children each time svg changes
    watch(selectedfcSumLayer, () => {
      hideSVGChildren("#fc-true-false-rw-svg")
    });

    // Declare behavior on mounted
    // functions called here
    onMounted(() => {
        hideSVGChildren("#fc-true-false-rw-svg");
        // update figure based on radio button selection
        getCurrentSVG();
    });

    async function hideSVGChildren(svgId) {
      await nextTick();
      d3.select(svgId).selectChildren()
        .attr("aria-hidden", true)
    }

    function getCurrentSVG() {
      const svgs = {
        tablet: {
          RW_noDrought: fcsumNDPlotTablet,
          'RW-all': fcsumRWPlotTablet,
          'RW-drought': fcsumYDPlotTablet
        },
        mobile: {
          RW_noDrought: fcsumNDPlotMobile,
          'RW-all': fcsumRWPlotMobile,
          'RW-drought': fcsumYDPlotMobile
        },
        desktop: {
          RW_noDrought: fcsumNDPlotDesktop,
          'RW-all': fcsumRWPlotDesktop,
          'RW-drought': fcsumYDPlotDesktop
        }
      }

      if (tabletView) {
        return svgs.tablet[selectedfcSumLayer.value];
      } else if (mobileView) {
        return svgs.mobile[selectedfcSumLayer.value];
      } else {
        return svgs.desktop[selectedfcSumLayer.value];
      }
    }
</script>

<style scoped lang="scss">
    #fc-true-false-rw-grid-container {
        display: grid;
        width: 100%;
        max-width: 800px;
        margin: 1rem auto 0rem auto;
        grid-template-areas:
            "chart";
    }
    #fc-true-false-rw-svg {
        grid-area: chart;
        place-self: center;
        height: 100%;
        width: 100%;
    }
</style>
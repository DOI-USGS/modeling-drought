<template>
  <VizSection
    id="loss-function"
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
      <p v-html="text.paragraph2" />
      <div class="toggle-container">
        <ToggleSwitch 
          v-for="layer, index in layers"
          :key="index"
          v-model="layer.visible" 
          :label="layer.label"
          :right-color="layer.color"
        />
      </div>
    </template>
    <template #figures>
      <div id="lf-grid-container">
        <lfPlotTablet
          v-if="tabletView"
          id="lf-svg"
        />
        <lfPlotMobile
          v-else-if="mobileView"
          id="lf-svg"
        />
        <lfPlotDesktop
          v-else
          id="lf-svg"
        />
      </div>
    </template>
    <!-- FIGURE CAPTION -->
    <template #figureCaption>
      <p v-if="tabletView" v-html="text.caption1Responsive" />
      <p v-else-if="mobileView" v-html="text.caption1Responsive" />
      <p v-else v-html="text.caption1Desktop" />
    </template>
    <!-- EXPLANATION -->
    <template #belowExplanation>
      <p v-html="text.paragraph3" />
    </template>
  </VizSection>
</template>

<script setup>
    import { onMounted, reactive, watch } from "vue";
    import * as d3 from 'd3';
    import { isMobile } from 'mobile-device-detect';
    import { isTablet } from 'mobile-device-detect';
    import VizSection from '@/components/VizSection.vue';
    import ToggleSwitch from "@/components/ToggleSwitch.vue"
    import lfPlotDesktop from "@/assets/svgs/lf_example_desktop.svg";
    import lfPlotTablet from "@/assets/svgs/lf_example_tablet.svg";
    import lfPlotMobile from "@/assets/svgs/lf_example_mobile.svg";

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

    // set up reactive variables
    const layers = reactive([
        {
            label: 'Observations',
            id: 'observation',
            visible: false,
            color: 'var(--color-observations)'
        },
        {
            label: '95% Quantile',
            id: 'UPPER',
            visible: false,
            color: 'var(--color-quantile-95)'
        },
        {
            label: 'Median',
            id: 'MEDIAN',
            visible: false,
            color: 'var(--color-median)'
        },
        {
            label: '5% Quantile',
            id: 'LOWER',
            visible: true,
            color: 'var(--color-quantile-5)'
        }
    ]);

    // Watches layers for changes and updates figure layers
    watch(layers, () => {
        updateFigure();
    });

    // Declare behavior on mounted
    // functions called here
    onMounted(() => {
        updateFigure();
        addInteractions();
    });
    
    function updateFigure() {
        layers.map(layer => {
            const targetOpacity = layer.visible ? 1 : 0;
            toggleLayer(layer.id, targetOpacity)
        })
    }

    function toggleLayer(targetID, targetOpacity) {
        if (targetID == 'observation') {
            d3.select("#" + targetID + "-full-lf").selectAll("path")
                .style("stroke-opacity", targetOpacity);
        } else {
            d3.select("#" + targetID + "-FORECAST-LINE").selectAll("path")
                    .style("stroke-opacity", targetOpacity);
            d3.select("#" + targetID +  "-LF-LINE").selectAll("path")
                .style("stroke-opacity", targetOpacity);
        }
    }

    // Draw the paired loss function and forecast lines
    function draw_paired_lines(line_id) {
        d3.select("#LF-" + line_id).selectAll("path")
            .style("stroke-opacity", 1)
        d3.select("#FORECAST-" + line_id).selectAll("path")
            .style("stroke-opacity", 1)
    }

    // Remove the paired loss function and forecast lines
    function remove_paired_lines(line_id) {
        d3.select("#LF-" + line_id).selectAll("path")
            .style("stroke-opacity", 0)
        d3.select("#FORECAST-" + line_id).selectAll("path")
            .style("stroke-opacity", 0)
    }

    // Function when mouse is over plot, moving on item
    function mouseover(event) {
        // if hovered over loss function line
        if (event.currentTarget.id.startsWith("LF")){
            let line_id = event.currentTarget.id.slice(3);
            draw_paired_lines(line_id);
        }
        // if hovered over forecast line
        if (event.currentTarget.id.startsWith("FORECAST")){
            let line_id = event.currentTarget.id.slice(9);
            draw_paired_lines(line_id);
        }
      }

    // Function when mouse is over plot, moving off item
    function mouseout(event) {
        // if hovered away from loss function line
        if (event.currentTarget.id.startsWith("LF")){
            let line_id = event.currentTarget.id.slice(3);
            remove_paired_lines(line_id)
        }
        // if hovered away from forecast line
        if (event.currentTarget.id.startsWith("FORECAST")){
            let line_id = event.currentTarget.id.slice(9);
            remove_paired_lines(line_id)
        }
    }

    function annotation(opacity){
        d3.select("#annotation_lossfunction").selectAll("text")
            .style("opacity", opacity);
        d3.select("#annotation_lossfunction_arrow").selectAll("path")
            .style("opacity", opacity);
        d3.select("#annotation_buttons1").selectAll("text")
            .style("opacity",opacity);
        for(let i=1;i<=4;i++){
            d3.select("#annotation_buttons1_arrow"+i.toString()).selectAll("path")
                .style("opacity", opacity);
        }
    }

    // when mouse leaves plot
    function mouseleave() {
        // add annotations
        annotation(1.0)
    }

    // when mouse enters plot
    function mouseenter() {
        // add annotations
        annotation(0.0)
    }

    function addInteractions() {
        // set viewbox for svg with loss function chart
        const lfSVG = d3.select("#lf-svg")

        // Add interaction to loss function chart
        lfSVG.select("#figure-lossfunction")
            .on("mouseleave", () => mouseleave())
            .on("mouseenter", () => mouseenter());

        lfSVG.selectAll("g")
            .on("mouseover", (event) => mouseover(event))
            .on("mouseout", (event) => mouseout(event))
    }
</script>

<style scoped lang="scss">
    #lf-grid-container {
        display: grid;
        width: 100%;
        max-width: 1200px;
        margin: 3rem auto 4rem auto;
        grid-template-areas:
            "chart";
    }
    #lf-svg {
        grid-area: chart;
        place-self: center;
        height: 100%;
        width: 100%;
    }
</style>
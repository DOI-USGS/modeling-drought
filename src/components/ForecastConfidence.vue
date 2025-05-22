<template>
  <VizSection
    id="forecast"
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
      <div id="fc-grid-container">
        <fcPlot
          id="fc-svg"
        />
      </div>
    </template>
    <!-- FIGURE CAPTION -->
    <template #figureCaption>
      <p
        v-if="tabletView"
        v-html="text.caption1Responsive"
      />
      <p
        v-else-if="mobileView"
        v-html="text.caption1Responsive"
      />
      <p
        v-else
        v-html="text.caption1Desktop"
      />
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
    import fcPlot from "@/assets/svgs/fc_example.svg";

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
            d3.select("#" + targetID + "-full-forecast").selectAll("path")
                .style("stroke-opacity", targetOpacity)
        } 
    }
    
    function draw_line(line_id_base,lookback) {
        for (let i = 0; i < lookback; i++) {
            let line_id = (parseInt(line_id_base) - i * 7).toString()
            let opacity = (lookback - i) / lookback
            //forecast lines
            d3.select("#forecast_middl_" + line_id).selectAll("path")
                .style("stroke-opacity", Math.pow(opacity,1.5))
                .style("stroke", d3.interpolateCividis(1-opacity))
                .style("stroke-width",2.*opacity);
        }
        d3.select("#forecast_patch_" + line_id_base).selectAll("path")
            .style("fill", d3.rgb(0,0,0,0.0));
        d3.select("#observation_" + line_id_base).selectAll("path")
                .style("stroke-opacity", 1.0);
      }

    function remove_line(line_id_base,lookback) {
        for (let i = 0; i < lookback; i++) {
            let line_id = (parseInt(line_id_base) - i * 7).toString()
            d3.select("#forecast_middl_" + line_id).selectAll("path")
                .style("stroke-opacity", 0);
        }
        d3.select("#forecast_patch_" + line_id_base).selectAll("path")
            .style("fill", d3.rgb(0,0,0,0));
        d3.select("#observation_" + line_id_base).selectAll("path")
            .style("stroke-opacity", 0);
    }

    function mouseover(event,lookback) {
        if (event.currentTarget.id.startsWith("forecast_hover_")){
            d3.select("#"+event.currentTarget.id).selectAll("path")
                .style("stroke-opacity", 0.1);
            let line_id_base = event.currentTarget.id.slice(15);
            draw_line(line_id_base,lookback)
        }
    }

    function mouseout(event,lookback) {
        if (event.currentTarget.id.startsWith("forecast_hover_")){
            d3.select("#"+event.currentTarget.id).selectAll("path")
                .style("stroke-opacity", 0.0);
            let line_id_base = event.currentTarget.id.slice(15);
            remove_line(line_id_base,lookback)
        }
    }

    function annotation(opacity){
        d3.select("#annotation_forecast").selectAll("text")
            .style("opacity", opacity);
        d3.select("#annotation_forecast_arrow").selectAll("path")
            .style("opacity", opacity);
    }

    function mouseleave(default_line,lookback) {
        // draw default line
        draw_line(default_line,lookback);
        // add annotation
        annotation(1.0)
    }

    function mouseenter(default_line,lookback) {
        // remove default line
        remove_line(default_line,lookback)
        // remove annotation
        annotation(0.0)    
    }

    function addInteractions() {
        // set viewbox for svg with loss function chart
        const fcSVG = d3.select("#fc-svg")

        // plot parameters
        const lookback = 13
        var default_line = "13055"
        draw_line(default_line,lookback)

        // Add interaction to loss function chart
        fcSVG.select("#axis-forecast")
            .on("mouseleave", () => mouseleave(default_line,lookback))
            .on("mouseenter", () => mouseenter(default_line,lookback));
        fcSVG.selectAll("g")
            .on("mouseover", (event) => mouseover(event,lookback))
            .on("mouseout", (event) => mouseout(event,lookback))
    }
</script>

<style scoped lang="scss">
    #fc-grid-container {
        display: grid;
        width: 100%;
        max-width: 1200px;
        margin: 3rem auto 4rem auto;
        grid-template-areas:
            "chart";
    }
    #fc-svg {
        grid-area: chart;
        place-self: center;
        height: 100%;
        width: 100%;
    }
</style>
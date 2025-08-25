<template>
  <VizSection
    id="forecast-explore"
    :figures="true"
    :fig-caption="true"
  >
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
        <fcPlotTablet
          v-if="tabletView"
          id="fc-svg"
        />
        <fcPlotMobile
          v-else-if="mobileView"
          id="fc-svg"
        />
        <fcPlotDesktop
          v-else
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
    import { isMobileOnly } from 'mobile-device-detect';
    import { isTablet } from 'mobile-device-detect';
    import VizSection from '@/components/VizSection.vue';
    import ToggleSwitch from "@/components/ToggleSwitch.vue"
    import fcPlotDesktop from "@/assets/svgs/fc_example_desktop.svg";
    import fcPlotTablet from "@/assets/svgs/fc_example_tablet.svg";
    import fcPlotMobile from "@/assets/svgs/fc_example_mobile.svg";

    // global variables
    const mobileView = isMobileOnly;
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
            visible: true,
            color: 'var(--color-observations)'
        }
    ]);

    // Watches layers for changes and updates figure layers
    watch(layers, () => {
        updateFigure(d3.select("#fc-svg"));
    });

    // Declare behavior on mounted
    // functions called here
    onMounted(() => {
        updateFigure(d3.select("#fc-svg"));
        addInteractions();
    });

    function updateFigure(svg) {
        layers.map(layer => {
            const targetOpacity = layer.visible ? 1 : 0;
            toggleLayer(svg, layer.id, targetOpacity)
        })
    }

    function toggleLayer(svg, targetID, targetOpacity) {
        if (targetID == 'observation') {
            svg.select("#" + targetID + "-full-forecast").selectAll("path")
                .style("stroke-opacity", targetOpacity)
        } 
    }
    
    function draw_line(svg, line_id_base,lookback) {
        for (let i = 0; i < lookback; i++) {
            let line_id = (parseInt(line_id_base) - i * 7).toString()
            let opacity = (lookback - i) / lookback
            //forecast lines
            svg.select("#forecast_middl_" + line_id).selectAll("path")
                .style("stroke-opacity", Math.pow(opacity,1.5))
                .style("stroke", d3.interpolateCividis(1-opacity))
                .style("stroke-width",2.*opacity);
        }
        svg.select("#forecast_patch_" + line_id_base).selectAll("path")
            .style("fill", d3.rgb(0,0,0,0.0));
        svg.select("#observation_" + line_id_base).selectAll("path")
                .style("stroke-opacity", 1.0);
      }

    function remove_line(svg, line_id_base,lookback) {
        for (let i = 0; i < lookback; i++) {
            let line_id = (parseInt(line_id_base) - i * 7).toString()
            svg.select("#forecast_middl_" + line_id).selectAll("path")
                .style("stroke-opacity", 0);
        }
        svg.select("#forecast_patch_" + line_id_base).selectAll("path")
            .style("fill", d3.rgb(0,0,0,0));
        svg.select("#observation_" + line_id_base).selectAll("path")
            .style("stroke-opacity", 0);
    }

    function mouseover(svg, event,lookback) {
        if (event.currentTarget.id.startsWith("forecast_hover_")){
            svg.select("#"+event.currentTarget.id).selectAll("path")
                .style("stroke-opacity", 0.1);
            let line_id_base = event.currentTarget.id.slice(15);
            draw_line(svg, line_id_base,lookback)
        }
    }

    function mouseout(svg, event,lookback) {
        if (event.currentTarget.id.startsWith("forecast_hover_")){
            svg.select("#"+event.currentTarget.id).selectAll("path")
                .style("stroke-opacity", 0.0);
            let line_id_base = event.currentTarget.id.slice(15);
            remove_line(svg, line_id_base,lookback)
        }
    }

    function annotation_1(svg, opacity){
      if (mobileView == true){
        svg.select("#annotation-1-forecast-mobile").selectAll("text")
            .style("opacity", opacity);
        svg.select("#annotation-1-forecast-arrow-mobile").selectAll("path")
            .style("opacity", opacity);
      }else if (tabletView == true){
        svg.select("#annotation-1-forecast-tablet").selectAll("text")
            .style("opacity", opacity);
        svg.select("#annotation-1-forecast-arrow-tablet").selectAll("path")
            .style("opacity", opacity);
      }else{
        svg.select("#annotation-1-forecast").selectAll("text")
            .style("opacity", opacity);
        svg.select("#annotation-1-forecast-arrow").selectAll("path")
            .style("opacity", opacity);
      }
    }

    function annotation_2(svg, opacity){
      if (mobileView == true){
        svg.select("#annotation-2-forecast-mobile").selectAll("text")
            .style("opacity", opacity);
        svg.select("#annotation-2-forecast-arrow-mobile").selectAll("path")
            .style("opacity", opacity);
      }else if (tabletView == true){
        svg.select("#annotation-2-forecast-tablet").selectAll("text")
            .style("opacity", opacity);
        svg.select("#annotation-2-forecast-arrow-tablet").selectAll("path")
            .style("opacity", opacity);
      }else{
        svg.select("#annotation-2-forecast").selectAll("text")
            .style("opacity", opacity);
        svg.select("#annotation-2-forecast-arrow").selectAll("path")
            .style("opacity", opacity);
      }
    }

    function drought_line(svg,opacity){
        svg.select("#obsv-ad-line").selectAll("path")
            .style("stroke-opacity", opacity);
    }

    function mouseleave(svg, default_line,lookback) {
        // draw default line
        draw_line(svg, default_line,lookback);
        // add annotation
        annotation_1(svg, 1.0)
        // remove washout layer
        svg.select("#forecast-washout").selectAll("path")
            .style("fill-opacity", 0.0);
    }

    function mouseenter(svg, default_line,lookback) {
        // remove default line
        remove_line(svg, default_line,lookback)
        // remove annotation
        annotation_1(svg, 0.0)   
        // add washout layer
        svg.select("#forecast-washout").selectAll("path")
            .style("fill-opacity", 0.75); 
    }

    function addInteractions() {
        // set viewbox for svg with loss function chart
        const fcSVG = d3.select("#fc-svg")

        // plot parameters
        const lookback = 13
        var default_line = "0"
        draw_line(fcSVG, default_line,lookback)

        // draw annotations
        annotation_1(fcSVG, 1.0)
        annotation_2(fcSVG, 1.0)

        // draw drought line
        drought_line(fcSVG, 1.0)

        // Add interaction to loss function chart
        fcSVG.select("#axis-forecast")
            .on("mouseleave", () => mouseleave(fcSVG, default_line,lookback))
            .on("mouseenter", () => mouseenter(fcSVG, default_line,lookback));
        fcSVG.selectAll("g")
            .on("mouseover", (event) => mouseover(fcSVG, event,lookback))
            .on("mouseout", (event) => mouseout(fcSVG, event,lookback))
    }
</script>

<style scoped lang="scss">
    #fc-grid-container {
        display: grid;
        width: 100%;
        max-width: 1200px;
        margin: 2rem auto 2rem auto;
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
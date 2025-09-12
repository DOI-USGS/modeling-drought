<template>
  <VizSection
    id="observation-explore"
    :figures="true"
    :fig-caption="true"
  >
    <template #aboveExplanation>
      <p v-html="text.paragraph1" />
    </template>
    <template #figures>
      <div id="obsv-grid-container">
        <obsvPlotTablet
          v-if="tabletView"
          role="img"
          :id="svgId"
          :aria-label="text.ariaLabel"
        />
        <obsvPlotMobile
          v-else-if="mobileView"
          role="img"
          :id="svgId"
          :aria-label="text.ariaLabel"
        />
        <obsvPlotDesktop
          v-else
          role="img"
          :id="svgId"
          :aria-label="text.ariaLabel"
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
    import { onMounted } from "vue";
    import * as d3 from 'd3';
    import { isMobileOnly } from 'mobile-device-detect';
    import { isTablet } from 'mobile-device-detect';
    import VizSection from '@/components/VizSection.vue';
    import obsvPlotDesktop from "@/assets/svgs/fc_example_desktop.svg";
    import obsvPlotTablet from "@/assets/svgs/fc_example_tablet.svg";
    import obsvPlotMobile from "@/assets/svgs/ob_example_mobile.svg";

    // global variables
    const mobileView = isMobileOnly;
    const tabletView = isTablet;
    const svgId = "obsv-svg"

    // define props
    const props = defineProps({
        text: { 
            type: Object,
            default() {
                return {}
            } 
        }
    })

    // Declare behavior on mounted
    // functions called here
    onMounted(() => {
       hideSVGChildren(svgId);
       addSVGDesc(svgId);
       addInteractions(svgId);
    });

    function hideSVGChildren(svgId) {
      d3.select(`#${svgId}`).selectChildren()
        .attr("aria-hidden", true)
    }

    function addSVGDesc(svgId) {
      d3.select(`#${svgId}`).append('desc')
        .attr("id", `${svgId}-desc`)
        .text(props.text.ariaDesc)
    }
    
    function draw_line(svg, line_id_base) {
        svg.select("#observation_" + line_id_base).selectAll("path")
                .style("stroke-opacity", 1.0);
      }

    function remove_line(svg, line_id_base) {
        svg.select("#observation_" + line_id_base).selectAll("path")
            .style("stroke-opacity", 0);
    }

    function mouseover(svg, event) {
        if (event.currentTarget.id.startsWith("forecast_hover_")){
            svg.select("#"+event.currentTarget.id).selectAll("path")
                .style("stroke-opacity", 0.1);
            let line_id_base = event.currentTarget.id.slice(15);
            draw_line(svg, line_id_base)
        }
    }

    function mouseout(svg, event) {
        if (event.currentTarget.id.startsWith("forecast_hover_")){
            svg.select("#"+event.currentTarget.id).selectAll("path")
                .style("stroke-opacity", 0.0);
            let line_id_base = event.currentTarget.id.slice(15);
            remove_line(svg, line_id_base)
        }
    }

    function annotation(svg, opacity){
      if (mobileView == true){
        svg.select("#annotation-1-observation-mobile").selectAll("text")
            .style("opacity", opacity);
        svg.select("#annotation-1-observation-arrow-mobile").selectAll("path")
            .style("opacity", opacity);
      }else if (tabletView == true){
        svg.select("#annotation-1-observation-tablet").selectAll("text")
            .style("opacity", opacity);
        svg.select("#annotation-1-observation-arrow-tablet").selectAll("path")
            .style("opacity", opacity);
      }else{
        svg.select("#annotation-1-observation").selectAll("text")
            .style("opacity", opacity);
        svg.select("#annotation-1-observation-arrow").selectAll("path")
            .style("opacity", opacity);
      }
    }

    function drought_labels(svg,opacity){
      if (mobileView == true){
        svg.select("#obsv-nm-label-mobile").selectAll("text")
            .style("opacity", opacity);
        svg.select("#obsv-ad-label-mobile").selectAll("text")
            .style("opacity", opacity);
        svg.select("#obsv-ad-line-mobile").selectAll("path")
            .style("stroke-opacity", opacity);
        svg.select("#obsv-ad-slopeline-mobile").selectAll("path")
            .style("stroke-opacity", opacity);
        svg.select("#obsv-md-label-mobile").selectAll("text")
            .style("opacity", opacity);
        svg.select("#obsv-md-line-mobile").selectAll("path")
            .style("stroke-opacity", opacity);
        svg.select("#obsv-md-slopeline-mobile").selectAll("path")
            .style("stroke-opacity", opacity);
        svg.select("#obsv-sd-label-mobile").selectAll("text")
            .style("opacity", opacity);
        svg.select("#obsv-sd-line-mobile").selectAll("path")
            .style("stroke-opacity", opacity);
        svg.select("#obsv-sd-slopeline-mobile").selectAll("path")
            .style("stroke-opacity", opacity);
        svg.select("#obsv-ed-label-mobile").selectAll("text")
            .style("opacity", opacity);
        svg.select("#obsv-ed-line-mobile").selectAll("path")
            .style("stroke-opacity", opacity);
        svg.select("#obsv-ed-slopeline-mobile").selectAll("path")
            .style("stroke-opacity", opacity);
      }else if (tabletView == true){
        svg.select("#obsv-nm-label-tablet").selectAll("text")
            .style("opacity", opacity);
        svg.select("#obsv-ad-label-tablet").selectAll("text")
            .style("opacity", opacity);
        svg.select("#obsv-ad-line-tablet").selectAll("path")
            .style("stroke-opacity", opacity);
        svg.select("#obsv-md-label-tablet").selectAll("text")
            .style("opacity", opacity);
        svg.select("#obsv-md-line-tablet").selectAll("path")
            .style("stroke-opacity", opacity);
        svg.select("#obsv-sd-label-tablet").selectAll("text")
            .style("opacity", opacity);
        svg.select("#obsv-sd-line-tablet").selectAll("path")
            .style("stroke-opacity", opacity);
        svg.select("#obsv-ed-label-tablet").selectAll("text")
            .style("opacity", opacity);
        svg.select("#obsv-ed-line-tablet").selectAll("path")
            .style("stroke-opacity", opacity);
      }else{
        svg.select("#obsv-nm-label").selectAll("text")
            .style("opacity", opacity);
        svg.select("#obsv-ad-label").selectAll("text")
            .style("opacity", opacity);
        svg.select("#obsv-ad-line").selectAll("path")
            .style("stroke-opacity", opacity);
        svg.select("#obsv-md-label").selectAll("text")
            .style("opacity", opacity);
        svg.select("#obsv-md-line").selectAll("path")
            .style("stroke-opacity", opacity);
        svg.select("#obsv-sd-label").selectAll("text")
            .style("opacity", opacity);
        svg.select("#obsv-sd-line").selectAll("path")
            .style("stroke-opacity", opacity);
        svg.select("#obsv-ed-label").selectAll("text")
            .style("opacity", opacity);
        svg.select("#obsv-ed-line").selectAll("path")
            .style("stroke-opacity", opacity);
      }
    }

    function mouseleave(svg, default_line) {
        // draw default line
        draw_line(svg, default_line);
        // add annotation
        annotation(svg, 1.0)
        svg.select("#observation-full-forecast").selectAll("path")
            .style("stroke-opacity", 0.0)
    }

    function mouseenter(svg, default_line) {
        // remove default line
        remove_line(svg, default_line)
        // remove annotation
        annotation(svg, 0.0)   
    }

    function addInteractions(svgId) {
        // set viewbox for svg with loss function chart
        const obsvSVG = d3.select(`#${svgId}`)

        // plot parameters
        var default_line = "70"
        draw_line(obsvSVG, default_line)

        // draw annotations
        annotation(obsvSVG, 1.0)

        // remove full observation line
        obsvSVG.select("#observation-full-forecast").selectAll("path")
            .style("stroke-opacity", 0.0);

        // remove title
        obsvSVG.select("#observation-forecast-title").selectAll("text")
            .style("opacity",0.0);

        // remove legend
        for (let i = 0; i <= 4; i++) {
        obsvSVG.select(`#forecast-legend-${i}`)
            .selectAll('path, text')
            .style('opacity', 0.0);
        }
        
        // add drought categories
        drought_labels(obsvSVG, 1.0)
        
        // Add interaction to loss function chart
        obsvSVG.select("#axis-forecast")
            .on("mouseleave", () => mouseleave(obsvSVG,default_line))
            .on("mouseenter", () => mouseenter(obsvSVG,default_line));
        obsvSVG.selectAll("g")
            .on("mouseover", (event) => mouseover(obsvSVG,event))
            .on("mouseout", (event) => mouseout(obsvSVG,event));
    }
</script>

<style scoped lang="scss">
    #obsv-grid-container {
        display: grid;
        width: 100%;
        max-width: 1200px;
        margin: 2rem auto 2rem auto;
        grid-template-areas:
            "chart";
    }
    #obsv-svg {
        grid-area: chart;
        place-self: center;
        height: 100%;
        width: 100%;
    }
</style>
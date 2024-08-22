<template>
    <VizSection
        id="forecast"
        :figures="true"
        :fig-caption="true"
    >
        <!-- HEADING -->
        <template #heading>
            <h2>
                {{ text.heading }}
            </h2>
        </template>
        <!-- FIGURES -->
        <template #aboveExplanation>
            <p v-html="text.paragraph1" />
            <p v-html="text.paragraph2" />
        </template>

        <!-- Is this the simplest way to set an image? -->
        <template #figures>
            <div id="fc-grid-container">
                <fcPlot
                    id="fc-svg"
                />
            </div>
        </template>
        <!-- FIGURE CAPTION -->
        <template #figureCaption>
        <p v-html="text.caption" />
        </template>
        <!-- EXPLANATION -->
        <template #belowExplanation>
            <p v-html="text.paragraph3" />
        </template>
    </VizSection>
</template>

<script setup>
    import { onMounted } from "vue";
    import * as d3 from 'd3';
    import VizSection from '@/components/VizSection.vue';
    import fcPlot from "@/assets/svgs/fc_example.svg";

    // define props
    defineProps({
        text: { type: Object }
    })

    // Declare behavior on mounted
    // functions called here
    onMounted(() => {
        addInteractions();
    });
    
    const lookback = 13

    function draw_line(line_id_base) {
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

    function remove_line(line_id_base) {
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

    function click(event) {
        if (event.currentTarget.id.startsWith("toggle-observations-forecast")){

            // get button distance changes
            let button_distance_y = d3.select("#shadow-toggle-observations-forecast").select("text").attr('y') - d3.select("#toggle-observations-forecast").select("text").attr('y');
            let button_distance_x = d3.select("#toggle-observations-forecast").select("text").attr('x') - d3.select("#shadow-toggle-observations-forecast").select("text").attr('x');

            // is button pressed or not
            let pressed_distance = parseFloat(d3.select("#toggle-observations-forecast").attr('transform').split(',')[1])
            if (pressed_distance == 0){
                d3.select("#toggle-observations-forecast").attr('transform','translate(0,'+button_distance_y.toString()+')');
                d3.select("#shadow-toggle-observations-forecast").attr('transform','translate('+button_distance_x.toString()+',0)');
            } else {
                d3.select("#toggle-observations-forecast").attr('transform','translate(0,0)');
                d3.select("#shadow-toggle-observations-forecast").attr('transform','translate(0,0)');
            }

            //observation line toggle
            let observation_opacity = 1.0;
            if (d3.select("#observation-full-forecast").selectAll("path").style("stroke-opacity") == 0){
                d3.select("#observation-full-forecast").selectAll("path")
                    .style("stroke-opacity", observation_opacity);
            } else if (d3.select("#observation-full-forecast").selectAll("path").style("stroke-opacity") == observation_opacity){
                d3.select("#observation-full-forecast").selectAll("path")
                    .style("stroke-opacity", 0);
            }
        }
    }

    function mouseover(event) {
        if (event.currentTarget.id.startsWith("forecast_hover_")){
            d3.select("#"+event.currentTarget.id).selectAll("path")
                .style("stroke-opacity", 0.1);
            let line_id_base = event.currentTarget.id.slice(15);
            draw_line(line_id_base)
        }
    }

    function mouseout(event) {
        if (event.currentTarget.id.startsWith("forecast_hover_")){
            d3.select("#"+event.currentTarget.id).selectAll("path")
                .style("stroke-opacity", 0.0);
            let line_id_base = event.currentTarget.id.slice(15);
            remove_line(line_id_base)
        }
    }

    function mouseleave(event,default_line) {
        if (event.currentTarget.id.startsWith("axis-forecast")){
            draw_line(default_line)        
            d3.select("#annotation_forecast").selectAll("text")
                .style("opacity", 1);
            d3.select("#annotation_forecast_arrow").selectAll("path")
                .style("opacity", 1);
            d3.select("#annotation_buttons3").selectAll("text")
                .style("opacity",1);
            d3.select("#annotation_buttons3_arrow1").selectAll("path")
                .style("opacity", 1);
        }
    }

    function mouseenter(event,default_line) {
        if (event.currentTarget.id.startsWith("axis-forecast")){
            remove_line(default_line)
            d3.select("#annotation_forecast").selectAll("text")
                .style("opacity", 0);
            d3.select("#annotation_forecast_arrow").selectAll("path")
                .style("opacity", 0);
            d3.select("#annotation_buttons3").selectAll("text")
                .style("opacity",0);
            d3.select("#annotation_buttons3_arrow1").selectAll("path")
                .style("opacity", 0);
        }
    }

    function addInteractions() {
        // set viewbox for svg with loss function chart
        const fcSVG = d3.select("#fc-svg")

        var default_line = "13055"
        draw_line(default_line)

        // set initial button transform, fills the attributes
        d3.select("#toggle-observations-forecast").attr('transform','translate(0,0)');
        d3.select("#shadow-toggle-observations-forecast").attr('transform','translate(0,0)');

        // Add interaction to loss function chart
        fcSVG.selectAll("g")
            .on("mouseover", (event) => mouseover(event))
            .on("mouseout", (event) => mouseout(event))
            .on("mouseleave", (event) => mouseleave(event,default_line))
            .on("mouseenter", (event) => mouseenter(event,default_line))
            .on("click", (event) => click(event))
    }
</script>

<style scoped lang="scss">
    #fc-grid-container {
        display: grid;
        width: 100%;
        max-width: 1200px;
        margin: 0 auto 0 auto;
        grid-template-areas:
            "chart";
    }
    #fc-svg {
        grid-area: chart;
        place-self: center;
        max-height: 80%;
        max-width: 80%;
    }
</style>
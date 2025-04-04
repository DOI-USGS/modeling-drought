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
        loopThroughElements(); // Start the loop
    });

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

    function click(switchoff) {
        // switch off the button no matter what if in the switchoff mode (true)
        if (switchoff === true) {
                d3.select("#toggle-observations-forecast").attr('transform','translate(0,0)');
                d3.select("#shadow-toggle-observations-forecast").attr('transform','translate(0,0)');
                d3.select("#observation-full-forecast").selectAll("path")
                    .style("stroke-opacity", 0);
        }
        else {
            // get button distance changes
            let button_distance_y = d3.select("#shadow-toggle-observations-forecast").select("text").attr('y') - d3.select("#toggle-observations-forecast").select("text").attr('y');
            let button_distance_x = d3.select("#toggle-observations-forecast").select("text").attr('x') - d3.select("#shadow-toggle-observations-forecast").select("text").attr('x');
        
            let pressed_distance = parseFloat(d3.select("#toggle-observations-forecast").attr('transform').split(',')[1]);
            // is button pressed or not
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

    function annotation1(opacity){
        d3.select("#annotation_forecast").selectAll("text")
            .style("opacity", opacity);
        d3.select("#annotation_forecast_arrow").selectAll("path")
            .style("opacity", opacity);
    }

    function annotation2(opacity){
        d3.select("#annotation_buttons3").selectAll("text")
            .style("opacity",opacity);
        d3.select("#annotation_buttons3_arrow1").selectAll("path")
            .style("opacity", opacity);
    }

    function addInteractions() {
        // set viewbox for svg with loss function chart
        const fcSVG = d3.select("#fc-svg")

        // set initial button transform, fills the attributes
        d3.select("#toggle-observations-forecast").attr('transform','translate(0,0)');
        d3.select("#shadow-toggle-observations-forecast").attr('transform','translate(0,0)');

        annotation1(0.0)   
        annotation2(1.0)   

        fcSVG.select("#toggle-observations-forecast")
            .on("click", () => click(false));
    }

    const lookback = 13;
    const totalElements = 13783;
    let currentIndex = 13055;

    function loopThroughElements() {
        draw_line((currentIndex).toString(),lookback);
        remove_line("13783",lookback);

        currentIndex++;
        if (currentIndex > totalElements) {
            currentIndex = 13055; 
        }

        requestAnimationFrame(loopThroughElements);
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
<style>
    #toggle-observations-forecast {
        cursor: pointer;
    }
    #shadow-toggle-observations-forecast {
        cursor: default;
    }
</style>


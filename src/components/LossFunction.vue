<template>
    <VizSection
        id="loss-function"
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
            <div id="lf-grid-container">
                <lfPlot
                    id="lf-svg"
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
    import lfPlot from "@/assets/svgs/lf_example.svg";

    // define props
    defineProps({
        text: { type: Object }
    })

    // Declare behavior on mounted
    // functions called here
    onMounted(() => {
        addInteractions();
    });
    
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
        // if hovered over buttons
        if (event.currentTarget.id.endsWith("-TAG") && event.currentTarget.id.startsWith("shadow") == false){
            // get ids
            let current_id = event.currentTarget.id;
            let shadow_id = 'shadow-' + event.currentTarget.id;
            // get button distance changes
            let button_distance_y = d3.select("#"+shadow_id).select("text").attr('y') - d3.select("#"+current_id).select("text").attr('y');
            let button_distance_x = d3.select("#"+current_id).select("text").attr('x') - d3.select("#"+shadow_id).select("text").attr('x');

            // move button down
            d3.select("#"+current_id).attr('transform','translate(0,'+button_distance_y.toString()+')');
            // move shadow under button
            d3.select("#"+shadow_id).attr('transform','translate('+button_distance_x.toString()+',0)');
            // draw corresponding lines
            let line_id = event.currentTarget.id.slice(0, -4);
            d3.select("#" + line_id + "-FORECAST-LINE").selectAll("path")
                .style("stroke-opacity", 1);
            d3.select("#" + line_id +  "-LF-LINE").selectAll("path")
                .style("stroke-opacity", 1);
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
        // if hovered away from buttons
        if (event.currentTarget.id.endsWith("TAG") && event.currentTarget.id.startsWith("shadow") == false){
            // get ids
            let current_id = event.currentTarget.id;
            let shadow_id = 'shadow-' + event.currentTarget.id;
            // move button up
            d3.select("#"+current_id).attr('transform','translate(0,0)');
            // move shadow out
            d3.select("#"+shadow_id).attr('transform','translate(0,0)');
            // remove corresponding lines
            let line_id = event.currentTarget.id.slice(0, -4);
            d3.select("#" + line_id + "-FORECAST-LINE").selectAll("path")
                .style("stroke-opacity", 0);
            d3.select("#" + line_id +  "-LF-LINE").selectAll("path")
                .style("stroke-opacity", 0);
        }
    }

    // when mouse is clicked
    function click(switchoff) {
        // switch off the button no matter what if in the switchoff mode (true)
        if (switchoff === true) {
            d3.select("#toggle-observations-lf").attr('transform','translate(0,0)');
            d3.select("#shadow-toggle-observations-lf").attr('transform','translate(0,0)');
            d3.select("#observation-full-lf").selectAll("path")
                .style("stroke-opacity", 0);
        }
        else{
            // get button distance changes
            let button_distance_y = d3.select("#shadow-toggle-observations-lf").select("text").attr('y') - d3.select("#toggle-observations-lf").select("text").attr('y');
            let button_distance_x = d3.select("#toggle-observations-lf").select("text").attr('x') - d3.select("#shadow-toggle-observations-lf").select("text").attr('x');

            // is button pressed or not
            let pressed_distance = parseFloat(d3.select("#toggle-observations-lf").attr('transform').split(',')[1])
            if (pressed_distance == 0){
                d3.select("#toggle-observations-lf").attr('transform','translate(0,'+button_distance_y.toString()+')');
                d3.select("#shadow-toggle-observations-lf").attr('transform','translate('+button_distance_x.toString()+',0)');
            } else {
                d3.select("#toggle-observations-lf").attr('transform','translate(0,0)');
                d3.select("#shadow-toggle-observations-lf").attr('transform','translate(0,0)');
            }
            //observation line toggle
            let observation_opacity = 1.0;
            if (d3.select("#observation-full-lf").selectAll("path").style("stroke-opacity") == 0){
                d3.select("#observation-full-lf").selectAll("path")
                    .style("stroke-opacity", observation_opacity);
            } else if (d3.select("#observation-full-lf").selectAll("path").style("stroke-opacity") == observation_opacity){
                d3.select("#observation-full-lf").selectAll("path")
                    .style("stroke-opacity", 0);
            }
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
    function mouseleave(default_line) {
        // draw default line
        draw_paired_lines(default_line);
        // add annotations
        annotation(1.0)
        // remove observation
        click(true)
    }

    // when mouse enters plot
    function mouseenter(default_line) {
        // remove default line
        remove_paired_lines(default_line);
        // add annotations
        annotation(0.0)
    }

    function addInteractions() {
        // set viewbox for svg with loss function chart
        const lfSVG = d3.select("#lf-svg")

        // set default line
        let default_line = 0;
        draw_paired_lines(default_line);

        // set initial button transform, fills the attributes
        d3.select("#toggle-observations-lf").attr('transform','translate(0,0)');
        d3.select("#shadow-toggle-observations-lf").attr('transform','translate(0,0)');
        d3.select("#LOWER-TAG").attr('transform','translate(0,0)');
        d3.select("#shadow-LOWER-TAG").attr('transform','translate(0,0)');
        d3.select("#MEDIAN-TAG").attr('transform','translate(0,0)');
        d3.select("#shadow-MEDIAN-TAG").attr('transform','translate(0,0)');
        d3.select("#UPPER-TAG").attr('transform','translate(0,0)');
        d3.select("#shadow-UPPER-TAG").attr('transform','translate(0,0)');

        // Add interaction to loss function chart
        lfSVG.select("#figure-lossfunction")
            .on("mouseleave", () => mouseleave(default_line))
            .on("mouseenter", () => mouseenter(default_line));
        lfSVG.selectAll("#toggle-observations-lf")
            .on("click", () => click(false));
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

<style>
    #toggle-observations-lf {
        cursor: pointer;
    }
    #LOWER-TAG {
        cursor: default;
    }
    #MEDIAN-TAG {
        cursor: default;
    }
    #UPPER-TAG {
        cursor: default;
    }
    #shadow-toggle-observations-lf {
        cursor: default;
    }
    #shadow-LOWER-TAG {
        cursor: default;
    }
    #shadow-MEDIAN-TAG {
        cursor: default;
    }
    #shadow-UPPER-TAG {
        cursor: default;
    }
</style>
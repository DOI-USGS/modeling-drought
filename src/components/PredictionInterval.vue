<template>
    <VizSection
        id="confidence-interval"
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
        </template>

        <!-- Is this the simplest way to set an image? -->
        <template #figures>
            <div id="pi-grid-container">
                <ciPlot
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
    import { onMounted } from "vue";
    import * as d3 from 'd3';
    import VizSection from '@/components/VizSection.vue';
    import ciPlot from "@/assets/svgs/pi_example.svg";

    // define props
    defineProps({
        text: { type: Object }
    })

    // Declare behavior on mounted
    // functions called here
    onMounted(() => {
        addInteractions();
    });
    
    function mouseover(event) {
        if (event.currentTarget.id.startsWith("TAG")){
            let tag_id = event.currentTarget.id;
            d3.select("#" + tag_id + "-LABEL-BOLD").selectAll("text")
                .style("opacity", 1);
            let line_id = event.currentTarget.id.slice(4);
            d3.select("#PI-PATCH-" + line_id).selectAll("path")
                .style("fill-opacity", 0.5)
                .style("stroke-opacity", 1);
            d3.select("#PI-PATCH-LOWER-" + line_id).selectAll("path")
                .style("stroke-opacity", 1);
            d3.select("#PI-PATCH-UPPER-" + line_id).selectAll("path")
                .style("stroke-opacity", 1);
            d3.select("#LF-LOWER-" + line_id).selectAll("path")
                .style("stroke-opacity", 1);
            d3.select("#LF-UPPER-" + line_id).selectAll("path")
                .style("stroke-opacity", 1);
            let hrefval = d3.select("#PI-missed-" + line_id + " use").attr("xlink:href")
            d3.select("#PI-missed-" + line_id).select(hrefval)
                .style("stroke-opacity", 1);

            // get ids
            let shadow_id = 'shadow-' + event.currentTarget.id;
            // get button distance changes
            let button_distance_y = d3.select("#"+shadow_id).select("text").attr('y') - d3.select("#"+tag_id).select("text").attr('y');
            let button_distance_x = d3.select("#"+tag_id).select("text").attr('x') - d3.select("#"+shadow_id).select("text").attr('x');

            // move button down
            d3.select("#"+tag_id).attr('transform','translate(0,'+button_distance_y.toString()+')');
            // move shadow under button
            d3.select("#"+shadow_id).attr('transform','translate('+button_distance_x.toString()+',0)');
        }
      }

    function mouseout(event) {
        if (event.currentTarget.id.startsWith("TAG")){
            let tag_id = event.currentTarget.id;
            d3.select("#" + tag_id + "-LABEL-BOLD").selectAll("text")
                .style("opacity", 0);
            let line_id = event.currentTarget.id.slice(4);
            d3.select("#PI-PATCH-" + line_id).selectAll("path")
                .style("fill-opacity", 0)
                .style("stroke-opacity", 0);
            d3.select("#PI-PATCH-LOWER-" + line_id).selectAll("path")
                .style("stroke-opacity", 0);
            d3.select("#PI-PATCH-UPPER-" + line_id).selectAll("path")
                .style("stroke-opacity", 0);
            d3.select("#LF-LOWER-" + line_id).selectAll("path")
                .style("stroke-opacity", 0);
            d3.select("#LF-UPPER-" + line_id).selectAll("path")
                .style("stroke-opacity", 0);
            let hrefval = d3.select("#PI-missed-" + line_id + " use").attr("xlink:href")
            d3.select("#PI-missed-" + line_id).select(hrefval)
                .style("stroke-opacity", 0);

            // get ids
            let shadow_id = 'shadow-' + event.currentTarget.id;
            // move button back
            d3.select("#"+tag_id).attr('transform','translate(0,0)');
            // move shadow back
            d3.select("#"+shadow_id).attr('transform','translate(0,0)');
        }
    }

    function mouseleave(event) {
        if (event.currentTarget.id.startsWith("figure-predictioninterval")){
            d3.select("#annotation_buttons2").selectAll("text")
                .style("opacity",1);
            for(let i=1;i<=4;i++){
                d3.select("#annotation_buttons2_arrow"+i.toString()).selectAll("path")
                    .style("opacity", 1);
            }
        }
    }

    function mouseenter(event) {
        if (event.currentTarget.id.startsWith("figure-predictioninterval")){
            d3.select("#annotation_buttons2").selectAll("text")
                .style("opacity",0);
            for(let i=1;i<=4;i++){
                d3.select("#annotation_buttons2_arrow"+i.toString()).selectAll("path")
                    .style("opacity", 0);
            }
        }
    }
    function addInteractions() {
        // set viewbox for svg with confidence interval chart
        const lfSVG = d3.select("#pi-svg")

        // set initial button transform, fills the attributes
        d3.select("#TAG-MEDIAN").attr('transform','translate(0,0)');
        d3.select("#shadow-TAG-MEDIAN").attr('transform','translate(0,0)');
        d3.select("#TAG-0").attr('transform','translate(0,0)');
        d3.select("#shadow-TAG-0").attr('transform','translate(0,0)');
        d3.select("#TAG-1").attr('transform','translate(0,0)');
        d3.select("#shadow-TAG-1").attr('transform','translate(0,0)');
        d3.select("#TAG-2").attr('transform','translate(0,0)');
        d3.select("#shadow-TAG-2").attr('transform','translate(0,0)');

        // Add interaction to confidence interval chart
        lfSVG.selectAll("g")
            .on("mouseover", (event) => mouseover(event))
            .on("mouseout", (event) => mouseout(event))
            .on("mouseleave", (event) => mouseleave(event))
            .on("mouseenter", (event) => mouseenter(event))
    }
</script>

<style scoped lang="scss">
    #pi-grid-container {
        display: grid;
        width: 100%;
        max-width: 1200px;
        margin: 0 auto 0 auto;
        grid-template-areas:
            "chart";
    }
    #pi-svg {
        grid-area: chart;
        place-self: center;
        max-height: 80%;
        max-width: 80%;
    }
</style>
<style>
    #toggle-observations-lf {
        cursor: pointer;
    }
</style>
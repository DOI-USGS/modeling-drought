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
            <ToggleSwitch 
                v-for="layer, index in layers"
                :key="index"
                v-model="layer.visible" 
                :label="layer.label"
                :rightColor="layer.color"
            />
        </template>
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
    import { onMounted, reactive, watch } from "vue";
    import * as d3 from 'd3';
    import VizSection from '@/components/VizSection.vue';
    import ToggleSwitch from "@/components/ToggleSwitch.vue"
    import lfPlot from "@/assets/svgs/lf_example.svg";

    // define props
    defineProps({
        text: { type: Object }
    })

    // set up reactive variables
    const layers = reactive({
        observations: {
            label: 'Observations',
            visible: false,
            color: 'var(--color-observations)'
        },
        quantile95: {
            label: '95% Quantile',
            visible: false,
            id: 'UPPER',
            color: 'var(--color-quantile-95)'
        },
        median: {
            label: 'Median',
            visible: false,
            id: 'MEDIAN',
            color: 'var(--color-median)'
        },
        quantile5: {
            label: '5% Quantile',
            visible: true,
            id: 'LOWER',
            color: 'var(--color-quantile-5)'
        }
    });

    // Watches currentFilterOption for changes and updates map to use correct data field for paint
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
        const obsOpacity = layers.observations.visible ? 1 : 0;
        toggleObservations(obsOpacity)
        const upperOpacity = layers.quantile95.visible ? 1 : 0;
        toggleForecastLine(layers.quantile95.id, upperOpacity)
        const medianOpacity = layers.median.visible ? 1 : 0;
        toggleForecastLine(layers.median.id, medianOpacity)
        const lowerOpacity = layers.quantile5.visible ? 1 : 0;
        toggleForecastLine(layers.quantile5.id, lowerOpacity)
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

    function toggleObservations(targetOpacity) {
        d3.select("#observation-full-lf").selectAll("path")
            .style("stroke-opacity", targetOpacity);
    }
    function toggleForecastLine(targetID, targetOpacity) {
        d3.select("#" + targetID + "-FORECAST-LINE").selectAll("path")
                .style("stroke-opacity", targetOpacity);
            d3.select("#" + targetID +  "-LF-LINE").selectAll("path")
                .style("stroke-opacity", targetOpacity);
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
<template>
    <VizSection
        id="loss-function"
        :figures="true"
        :fig-caption="true"
    >
        <template #heading>
            <h2>{{ text.heading }}</h2>
        </template>
        <template #aboveExplanation>
            <p v-html="text.paragraph1" />
            <p v-html="text.paragraph2" />
        </template>
        <template #figures>
            <svg ref="svg" :width="width" :height="height"></svg>
        </template>
        <template #figureCaption>
            <p v-html="text.caption" />
        </template>
        <template #belowExplanation>
            <p v-html="text.paragraph3" />
        </template>
    </VizSection>
</template>

<script setup>
import { ref, onMounted } from "vue";
import * as d3 from 'd3';
import VizSection from '@/components/VizSection.vue';

// Importing images from assets
import Ellie from '@/assets/images/face.jpeg';
import Jeremy from '@/assets/images/face.jpeg';
import John from '@/assets/images/face.jpeg';
import Althea from '@/assets/images/face.jpeg';
import Caelan from '@/assets/images/face.jpeg';
import Scott from '@/assets/images/face.jpeg';
import Person from '@/assets/images/face.jpeg';

defineProps({
    text: { type: Object }
});

const width = 800;
const height = 600;
const colorHighlight = '#FF9F00';

const svg = ref(null);

const nodes = ref([
    { id: 'Ellie', group: 1, img: Ellie, url: 'https://www.usgs.gov/staff-profiles/elaheh-white' },
    { id: 'John', group: 2, img: John, url: 'https://www.usgs.gov/staff-profiles/john-c-hammond' },
    { id: 'Althea', group: 3, img: Althea, url: 'https://www.usgs.gov/staff-profiles/althea-a-archer' },
    { id: 'Caelan', group: 1, img: Caelan, url: 'https://www.usgs.gov/staff-profiles/elaheh-white' },
    { id: 'Jeremy', group: 2, img: Jeremy, url: 'https://www.usgs.gov/staff-profiles/elaheh-white' },
    { id: 'Scott', group: 3, img: Scott, url: 'https://www.usgs.gov/staff-profiles/elaheh-white' },
    { id: 'Person', group: 1, img: Person, url: 'https://www.usgs.gov/staff-profiles/elaheh-white' },
    { id: 'Jake', group: 2, img: Person, url: 'https://www.usgs.gov/staff-profiles/elaheh-white' }
]);

const edges = ref([]);

function generateEdges() {
    nodes.value.forEach((source, i) => {
        nodes.value.forEach((target, j) => {
            if (i !== j && Math.random() > 0.5) {
                edges.value.push({ source: source.id, target: target.id });
            }
        });
    });
}

onMounted(() => {
    generateEdges();
    drawGraph();
});

function drawGraph() {
    const nodeRadius = 40;
    const edgeWidth = 2;

    const simulation = d3.forceSimulation(nodes.value)
        .force('link', d3.forceLink(edges.value).id(d => d.id).distance(100))
        .force('charge', d3.forceManyBody().strength(-300))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('collision', d3.forceCollide().radius(nodeRadius*2));

    const svgElement = d3.select(svg.value);

    svgElement.append("defs").selectAll("clipPath")
        .data(nodes.value)
        .join("clipPath")
        .attr("id", d => `clip-${d.id}`)
        .append("circle")
        .attr("r", nodeRadius);

    const link = svgElement.append('g')
        .attr('stroke', 'black')
        .attr('stroke-opacity', 0.6)
        .selectAll('line')
        .data(edges.value)
        .join('line')
        .attr('stroke-width', edgeWidth);

    const node = svgElement.append('g')
        .selectAll('circle')
        .data(nodes.value)
        .join('circle')
        .attr('r', nodeRadius)
        .attr('stroke', "black")
        .attr('stroke-width', 4)
        .style('fill', d => `url(#pattern-${d.id})`);

    // Append images within patterns for filling circles
    const patterns = svgElement.append('defs')
        .selectAll('pattern')
        .data(nodes.value)
        .enter()
        .append('pattern')
        .attr('id', d => `pattern-${d.id}`)
        .attr('height', 1)
        .attr('width', 1)
        .attr('patternContentUnits', 'objectBoundingBox')
        .append('image')
        .attr('href', d => d.img)
        .attr('height', 1)
        .attr('width', 1)
        .attr('preserveAspectRatio', 'xMidYMid slice');

    // Text labels (hidden by default)
    const labels = svgElement.append('g')
        .selectAll('text')
        .data(nodes.value)
        .join('text')
        .text(d => d.id)
        .attr('x', d => d.x)
        .attr('y', d => d.y - nodeRadius - 10)
        .attr('text-anchor', 'middle')
        .style('visibility', 'hidden');

    // Mouse interaction behavior
    node.on('mouseover', (event, d) => {
        d3.select(event.currentTarget)
        .style('fill', 'orangered');
        labels.filter(ld => ld.id === d.id)
        .style('visibility', 'visible');
    })
    .on('mouseout', (event, d) => {
        d3.select(event.currentTarget)
        .style('fill', `url(#pattern-${d.id})`);
        labels.filter(ld => ld.id === d.id)
        .style('visibility', 'hidden');
    })
    .on('click', (event, d) => {
        window.open(d.url, '_blank');
     });


    simulation.on('tick', () => {
        link
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            .attr('x2', d => d.target.x)
            .attr('y2', d => d.target.y);

        node
            .attr('cx', d => d.x)
            .attr('cy', d => d.y);

        labels
            .attr('x', d => d.x)
            .attr('y', d => d.y);
    });

    function drag(simulation) {
        function dragstarted(event) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            event.subject.fx = event.subject.x;
            event.subject.fy = event.subject.y;
        }

        function dragged(event) {
            event.subject.fx = event.x;
            event.subject.fy = event.y;
        }

        function dragended(event) {
            if (!event.active) simulation.alphaTarget(0);
            event.subject.fx = null;
            event.subject.fy = null;
        }

        return d3.drag()
            .on('start', dragstarted)
            .on('drag', dragged)
            .on('end', dragended);
    }
}
</script>

<style scoped lang="scss">

</style>

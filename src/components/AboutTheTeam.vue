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
    { id: 'Ellie', group: 'IIDD', img: Ellie, url: 'https://www.usgs.gov/staff-profiles/elaheh-white' },
    { id: 'John', group: 'MD-DE-DC', img: John, url: 'https://www.usgs.gov/staff-profiles/john-c-hammond' },
    { id: 'Erik', group: 'OPP', img: John, url: 'https://www.usgs.gov/staff-profiles/erik-smith' },
    { id: 'Kaysa', group: 'IIDD', img: John, url: 'labs.waterdata.usgs.gov/visualizations' },
    { id: 'Jeffrey', group: 'IIDD', img: John, url: 'https://www.usgs.gov/staff-profiles/jeffrey-kwang' },
    { id: 'Cee', group: 'IIDD', img: John, url: 'https://www.usgs.gov/staff-profiles/cee-nell' },
    { id: 'Althea', group:  'IIDD', img: Althea, url: 'https://www.usgs.gov/staff-profiles/althea-a-archer' },
    { id: 'Caelan', group: 'OR', img: Caelan, url: 'https://www.usgs.gov/staff-profiles/caelan-e-simeone' },
    { id: 'Jeremy', group:  'IIDD', img: Jeremy, url: 'https://scholar.google.com/citations?user=roIN6vgAAAAJ' },
    { id: 'Scott', group: 'IMPD', img: Scott, url: 'https://www.usgs.gov/staff-profiles/scott-hamshaw' },
    { id: 'Philip', group: 'ESPD', img: Person, url: 'https://www.usgs.gov/staff-profiles/phillip-goodling' },
    { id: 'Roy', group: 'WY-MT', img: Person, url: 'https://www.usgs.gov/staff-profiles/roy-sando' },
    { id: 'Aaron', group: 'WY-MT', img: Person, url: 'https://www.usgs.gov/staff-profiles/aaron-j-heldmyer' },
    { id: 'Ryan', group: 'WY-MT', img: Person, url: 'https://www.usgs.gov/staff-profiles/ryan-r-mcshane' },
    { id: 'Bryce', group: 'UT', img: Person, url: 'https://www.usgs.gov/index.php/staff-profiles/bryce-pulver' },
    { id: 'Andrew', group: 'MD-DE-DC', img: Person, url: 'https://www.usgs.gov/staff-profiles/andrew-sekellick' },
    { id: 'Leah', group: 'MD-DE-DC', img: Person, url: 'https://www.usgs.gov/staff-profiles/leah-e-staub' },
    { id: 'David', group: 'IIDD', img: Person, url: 'https://www.usgs.gov/staff-profiles/david-watkins' },
    { id: 'Michael', group: 'MD-DE-DC', img: Person, url: 'https://www.usgs.gov/staff-profiles/michael-e-wieczorek' },
    { id: 'Kendall', group: 'MD-DE-DC', img: Person, url: 'https://www.usgs.gov/staff-profiles/jacob-zwart' },
    { id: 'Jake', group:  'IIDD', img: Person, url: 'https://www.usgs.gov/staff-profiles/elaheh-white' }
]);

const edges = ref([]);

function generateEdges() {
    nodes.value.forEach((source, i) => {
        nodes.value.forEach((target, j) => {
            if (i !== j && Math.random() > 0.5) {
                edges.value.push({ source: source.id, target: target.id, length: Math.random()*100 });
            }
        });
    });
}

onMounted(() => {
    generateEdges();
    drawGraph();
});

function drawGraph() {
    const nodeRadius = 30;
    const edgeWidth = 2;

    const simulation = d3.forceSimulation(nodes.value)
        .force('link', d3.forceLink(edges.value).id(d => d.id).distance(d => d.length))
        .force('charge', d3.forceManyBody().strength(d => -200 - Math.random() * 100))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('collision', d3.forceCollide().radius(nodeRadius * 2));

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
        .style('fill', d => `url(#pattern-${d.id})`)
        .call(drag(simulation));

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

    const labels = svgElement.append('g')
        .selectAll('text')
        .data(nodes.value)
        .join('text')
        .text(d => d.id)
        .attr('x', d => d.x)
        .attr('y', d => d.y - nodeRadius - 10)
        .attr('text-anchor', 'middle')
        .style('visibility', 'hidden');

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
            .attr('cx', d => {
            d.x = Math.max(nodeRadius, Math.min(width - nodeRadius, d.x));
            return d.x;
        })
            .attr('cy', d => {
            d.y = Math.max(nodeRadius, Math.min(height - nodeRadius, d.y));
            return d.y;
        });

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

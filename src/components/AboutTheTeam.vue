<template>
  <VizSection
    id="the-team"
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
      <div class="svg-container">
        <svg
          ref="svg"
          :width="width"
          :height="height"
        />
      </div>
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
import Person from '@/assets/images/face.jpeg';

defineProps({
    text: { 
      type: Object,
      default() {
        return {}
      } 
    }
});

const width = 800;
const height = 600;
const colorHighlight = '#FF9F00';

const svg = ref(null);


const nodes = ref([
    { id: 'Althea', name: 'Althea Archer', group:  'IIDD', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/media/images/aaarcher_staff_profile.jpg?h=585bdce6&itok=Z0LQ51Gs', url: 'https://www.usgs.gov/staff-profiles/althea-a-archer'},
    { id: 'Jeremy', name: 'Jeremy Diaz', group: 'IIDD', img: 'https://dfi09q69oy2jm.cloudfront.net/visualizations/headshots/jeremy_diaz.jpg', url: 'https://scholar.google.com/citations?user=roIN6vgAAAAJ'},
    { id: 'Philip', name: 'Phillip Goodling', group: 'ESPD', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/media/images/PXL_20220409_214211061~2.jpg?itok=OHgiDh8V', url: 'https://www.usgs.gov/staff-profiles/phillip-goodling' },
    { id: 'John', name: 'John Hammond', group: 'MD-DE-DC', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/media/images/john.hammond.png?h=eb4caff5&itok=FPW57mEo', url: 'https://www.usgs.gov/staff-profiles/john-c-hammond' },
    { id: 'Scott', name: 'Scott Hamshaw', group: 'IMPD', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/media/images/Hamshaw%20Photo_0.png?h=ffb9992a&itok=UwqGwPsX', url: 'https://www.usgs.gov/staff-profiles/scott-hamshaw' },
    { id: 'Aaron', name: 'Aaron Heldmyer', group: 'WY-MT', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/thumbnails/image/aaron_j_H.png?itok=zoE5JMoB', url: 'https://www.usgs.gov/staff-profiles/aaron-j-heldmyer' },
    { id: 'Jeffrey', name: 'Jeffrey Kwang', group: 'IIDD', img: 'https://dfi09q69oy2jm.cloudfront.net/visualizations/headshots/jeffrey_kwang_profile.png', url: 'https://www.usgs.gov/staff-profiles/jeffrey-kwang' },
    { id: 'Ryan', name: 'Ryan McShane', group: 'WY-MT', img: Person, url: 'https://www.usgs.gov/staff-profiles/ryan-r-mcshane' },
    { id: 'Cee', name: 'Cee Nell', group: 'IIDD', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/media/images/cee%20nell%20resized.png?h=53fbb397&itok=I7tqKZDm', url: 'https://www.usgs.gov/staff-profiles/cee-nell' },
    { id: 'Bryce', name: 'Bryce Pulver', group: 'UT', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/media/images/Bryce.jpg?h=3f136433&itok=NjoyKU5C', url: 'https://www.usgs.gov/staff-profiles/bryce-pulver' },
    { id: 'Jesse', name: 'Jesse Ross', group: 'IIDD', img: 'https://dfi09q69oy2jm.cloudfront.net/visualizations/headshots/jesse_ross.jpg', url: '' },
    { id: 'Roy', name: 'Roy Sando', group: 'WY-MT', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/thumbnails/image/gen70991PicForKathy.jpg?itok=nIlDArWf', url: 'https://www.usgs.gov/staff-profiles/roy-sando' },
    { id: 'Anteneh', name: 'Anteneh Sarbanes', group: 'MD-DE-DC', img: Person, url: '' },
    { id: 'Andrew', name: 'Andrew Sekellick', group: 'MD-DE-DC', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/thumbnails/image/me_3.jpg?itok=y70cpj2J', url: 'https://www.usgs.gov/staff-profiles/andrew-sekellick' },
    { id: 'Caelan', name: 'Caelan Simeone', group: 'OR', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/media/images/simeone_USGS_Profile.jpg?itok=tL8i5X5H', url: 'https://www.usgs.gov/staff-profiles/caelan-e-simeone' },
    { id: 'Erik', name: 'Erik Smith', group: 'OPP', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/thumbnails/image/SmithErik.png?itok=LJ-7BX9I', url: 'https://www.usgs.gov/staff-profiles/erik-smith' },
    { id: 'Leah', name: 'Leah Staub', group: 'MD-DE-DC', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/thumbnails/image/me2_1.jpg?itok=cA5khYdt', url: 'https://www.usgs.gov/staff-profiles/leah-e-staub' },
    { id: 'David', name: 'David Watkins', group: 'IIDD', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/media/images/Watkins_StaffProfile.png?h=ad04b26d&itok=Mve2MXjG', url: 'https://www.usgs.gov/staff-profiles/david-watkins' },
    { id: 'Michael', name: 'Michael Wieczorek', group: 'MD-DE-DC', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/thumbnails/image/MD_wieczorek.gif?itok=pzpIHaUG', url: 'https://www.usgs.gov/staff-profiles/michael-e-wieczorek' },
    { id: 'Kendall', name: 'Kendall Wnuk', group: 'MD-DE-DC', img: Person, url: 'https://www.usgs.gov/staff-profiles/kendall-wnuk' },
    { id: 'Jake', name: 'Jacob Zwart', group:  'IIDD', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/media/images/zwart-jacob.jpg?h=3d1375cf&itok=BCrm0TBr', url: 'https://www.usgs.gov/staff-profiles/jacob-zwart' },
    { id: 'Hayley', name: 'Hayley Corson-Dosch', group:  'IIDD', img: 'https://dfi09q69oy2jm.cloudfront.net/visualizations/headshots/HCorson-Dosch.png', url: 'https://www.usgs.gov/staff-profiles/hayley-corson-dosch'}
]);

const edges = ref([]);

// create centers for each grouping
const groupCenters = new Map();
const groupCount = new Set(nodes.value.map(d => d.group)).size;


// this function is generating random linkages between people using connectivity %
// 
function generateEdges() {
    nodes.value.forEach((source, i) => {
        nodes.value.forEach((target, j) => {
            if (i !== j) {
                const isSameGroup = source.group === target.group;
                const probability = isSameGroup ? 0.5 : 0.05;  // setting random levels of connectivity within : among group
                if (Math.random() < probability) {
                    edges.value.push({ source: source.id, target: target.id, length: isSameGroup ? 20 : 100 });
                }
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
    const edgeWidth = 0;

    // groups color scale
    const color = d3.scaleOrdinal(d3.schemeCategory10);

    const groupNames = [...new Set(nodes.value.map(d => d.group))];
    const groupCenters = new Map();
    const radius = Math.min(width, height) / 2.5;

    groupNames.forEach((group, i) => {
        const angle = (i / groupCount) * 2 * Math.PI;
        const cx = width / 2 + radius * Math.cos(angle);
        const cy = height / 2 + radius * Math.sin(angle);
        groupCenters.set(group, { x: cx, y: cy });
    });

    const simulation = d3.forceSimulation(nodes.value)
        .force('link', d3.forceLink(edges.value).id(d => d.id).distance(d => d.length))
        .force('charge', d3.forceManyBody().strength(d => -200 - Math.random() * 100))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('collision', d3.forceCollide().radius(nodeRadius * 2))
        .force('cluster', forceCluster(0.2));

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
        .attr('stroke', d => color(d.group))
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
        .style('visibility', 'hidden')
        .style('pointer-events', 'none');

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
            .attr('x1', d => constrain(d.source.x, nodeRadius, width - nodeRadius))
            .attr('y1', d => constrain(d.source.y, nodeRadius, height - nodeRadius))
            .attr('x2', d => constrain(d.target.x, nodeRadius, width - nodeRadius))
            .attr('y2', d => constrain(d.target.y, nodeRadius, height - nodeRadius));

        node
            .attr('cx', d => {
                d.x = constrain(d.x, nodeRadius, width - nodeRadius);
                return d.x;
            })
            .attr('cy', d => {
                d.y = constrain(d.y, nodeRadius, height - nodeRadius);
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
    function constrain(value, min, max) {
        return Math.max(min, Math.min(max, value));
    }

    function forceCluster() {
        const strength = 0.1;
        return alpha => {
            nodes.value.forEach(d => {
                const cluster = nodes.value.find(n => n.group === d.group);
                if (cluster && cluster !== d) {
                    const x = d.x - cluster.x;
                    const y = d.y - cluster.y;
                    const l = Math.sqrt(x * x + y * y);
                    const r = nodeRadius * 2;
                    if (l !== r) {
                        const ratio = (l - r) / l * alpha * strength;
                        d.vx -= x * ratio;
                        d.vy -= y * ratio;
                    }
                }
            });
        };
    }
}

</script>

<style scoped lang="scss">
.svg-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
}
</style>

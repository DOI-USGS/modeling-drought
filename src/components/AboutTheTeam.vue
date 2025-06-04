<template>
  <VizSection
    id="the-team"
    :figures="true"
    :fig-caption="true"
  >
    <template #heading>
      <h3>{{ text.heading }}</h3>
    </template>
    <template #aboveExplanation>
      <p v-html="text.paragraph1" />
      <p 
        class="extra-line-spacing" 
        v-html="text.paragraph2" 
      />
    </template>
    <template #figures>
      <div class="svg-container">
        <svg
          ref="svg"
          class="svg"
          :width="width"
          :height="height"
        />
      </div>
    </template>
  </VizSection>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
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

let width = 0;
let height = 0;
let nodeRadius = 45;

const svg = ref(null);

const nodes = ref([
    { id: 'Althea', name: 'Althea Archer', group:  'IIDD', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/media/images/aaarcher_staff_profile.jpg?h=585bdce6&itok=Z0LQ51Gs', url: 'https://www.usgs.gov/staff-profiles/althea-a-archer'},
    { id: 'Jeremy', name: 'Jeremy Diaz', group: 'IIDD', img: 'https://dfi09q69oy2jm.cloudfront.net/visualizations/headshots/jeremy_diaz.jpg', url: 'https://scholar.google.com/citations?user=roIN6vgAAAAJ'},
    { id: 'Philip', name: 'Phillip Goodling', group: 'ESPD', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/media/images/PXL_20220409_214211061~2.jpg?itok=OHgiDh8V', url: 'https://www.usgs.gov/staff-profiles/phillip-goodling' },
    { id: 'John', name: 'John Hammond', group: 'MD-DE-DC', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/media/images/john.hammond.png?h=eb4caff5&itok=FPW57mEo', url: 'https://www.usgs.gov/staff-profiles/john-c-hammond' },
    { id: 'Scott', name: 'Scott Hamshaw', group: 'IMPD', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/media/images/Hamshaw%20Photo_0.png?h=ffb9992a&itok=UwqGwPsX', url: 'https://www.usgs.gov/staff-profiles/scott-hamshaw' },
    { id: 'Aaron', name: 'Aaron Heldmyer', group: 'WY-MT', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/thumbnails/image/aaron_j_H.png?itok=zoE5JMoB', url: 'https://www.usgs.gov/staff-profiles/aaron-j-heldmyer' },
    { id: 'Jeffrey', name: 'Jeffrey Kwang', group: 'IIDD', img: 'https://dfi09q69oy2jm.cloudfront.net/visualizations/headshots/jeffrey_kwang_profile.png', url: 'https://www.usgs.gov/staff-profiles/jeffrey-kwang' },
    { id: 'Ryan', name: 'Ryan McShane', group: 'WY-MT', img: 'https://dfi09q69oy2jm.cloudfront.net/visualizations/headshots/ryan_mcshane.jpg', url: 'https://www.usgs.gov/staff-profiles/ryan-r-mcshane' },
    { id: 'Cee', name: 'Cee Nell', group: 'IIDD', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/media/images/cee%20nell%20resized.png?h=53fbb397&itok=I7tqKZDm', url: 'https://www.usgs.gov/staff-profiles/cee-nell' },
    { id: 'Bryce', name: 'Bryce Pulver', group: 'UT', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/media/images/Bryce.jpg?h=3f136433&itok=NjoyKU5C', url: 'https://www.usgs.gov/staff-profiles/bryce-pulver' },
    { id: 'Jesse', name: 'Jesse Ross', group: 'IIDD', img: 'https://dfi09q69oy2jm.cloudfront.net/visualizations/headshots/jesse_ross.jpg', url: '' },
    { id: 'Roy', name: 'Roy Sando', group: 'WY-MT', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/thumbnails/image/gen70991PicForKathy.jpg?itok=nIlDArWf', url: 'https://www.usgs.gov/staff-profiles/roy-sando' },
    { id: 'Anteneh', name: 'Anteneh Sarbanes', group: 'OSD', img: Person, url: '' },
    { id: 'Andrew', name: 'Andrew Sekellick', group: 'MD-DE-DC', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/thumbnails/image/me_3.jpg?itok=y70cpj2J', url: 'https://www.usgs.gov/staff-profiles/andrew-sekellick' },
    { id: 'Caelan', name: 'Caelan Simeone', group: 'OR', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/media/images/simeone_USGS_Profile.jpg?itok=tL8i5X5H', url: 'https://www.usgs.gov/staff-profiles/caelan-e-simeone' },
    { id: 'Erik', name: 'Erik Smith', group: 'OPP', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/thumbnails/image/SmithErik.png?itok=LJ-7BX9I', url: 'https://www.usgs.gov/staff-profiles/erik-smith' },
    { id: 'Leah', name: 'Leah Staub', group: 'MD-DE-DC', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/thumbnails/image/me2_1.jpg?itok=cA5khYdt', url: 'https://www.usgs.gov/staff-profiles/leah-e-staub' },
    { id: 'David', name: 'David Watkins', group: 'IIDD', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/media/images/Watkins_StaffProfile.png?h=ad04b26d&itok=Mve2MXjG', url: 'https://www.usgs.gov/staff-profiles/david-watkins' },
    { id: 'Michael', name: 'Michael Wieczorek', group: 'MD-DE-DC', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/thumbnails/image/MD_wieczorek.gif?itok=pzpIHaUG', url: 'https://www.usgs.gov/staff-profiles/michael-e-wieczorek' },
    { id: 'Kendall', name: 'Kendall Wnuk', group: 'MD-DE-DC', img: 'https://dfi09q69oy2jm.cloudfront.net/visualizations/headshots/Wnuk_Profile_Pic.jpg', url: 'https://www.usgs.gov/staff-profiles/kendall-wnuk' },
    { id: 'Jake', name: 'Jacob Zwart', group:  'IIDD', img: 'https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/styles/staff_profile/public/media/images/zwart-jacob.jpg?h=3d1375cf&itok=BCrm0TBr', url: 'https://www.usgs.gov/staff-profiles/jacob-zwart' },
    { id: 'Hayley', name: 'Hayley Corson-Dosch', group:  'IIDD', img: 'https://dfi09q69oy2jm.cloudfront.net/visualizations/headshots/HCorson-Dosch.png', url: 'https://www.usgs.gov/staff-profiles/hayley-corson-dosch'}
]);

// for group visual fx
const groupAuras = new Map();
const groupColors = ref({});
const colors = {
    IIDD: "var(--medium-blue)",
    ESPD: "var(--less-faded-usgs-blue)",
    "MD-DE-DC": "var(--dark-mustard)",
    IMPD: "var(--brighter-grey-blue)",
    "WY-MT": "var(--bright-mustard)",
    UT: "var(--medium-brown)",
    OSD: "var(--very-light-blue)",
    OR: "var(--tan)",
    OPP: "var(--medium-grey)"
}

onMounted(() => {
    resizeAndDraw();
    window.addEventListener('resize', resizeAndDraw);
});

// adjust the cluster space based on svg and screen 
function resizeAndDraw() {
  if (!svg.value) return;

  const bounds = svg.value.getBoundingClientRect();
  width = bounds.width;
  height = bounds.height;
  nodeRadius = Math.min(width, height) * 0.07;
  
  d3.select(svg.value).selectAll('*').remove();
  drawGraph();
}

// computed styles based on group colors
const groupStyles = computed(() => {
  return Object.entries(groupColors.value).map(([group, color]) => {
    return `.group-label:contains('${group}') { background-color: ${color}; color: white; padding: 0.1em 0.4em; border-radius: 4px; margin: 0 0.2em; }`;
  }).join('\n');
});

// inject dynamic style tag
watch(groupColors, () => {
  const style = document.getElementById('group-style') || document.createElement('style');
  style.id = 'group-style';

  style.innerHTML = Object.entries(groupColors.value).map(([group, color]) => {
    return `.group-label[data-group='${group}'] { background-color: ${color}; }`;
  }).join('\n');

  document.head.appendChild(style);
}, { immediate: true });


function drawGraph() {

    // for group positioning
    const groupNames = [...new Set(nodes.value.map(d => d.group))];
    const groupCenters = new Map();

    groupNames.forEach(group => {
        const cx = width / 2 + (Math.random() - 0.5) * width * 0.5;
        const cy = height / 2 + (Math.random() - 0.5) * height * 0.5;
        groupCenters.set(group, { x: cx, y: cy });
    });

    function updateGroupColors() {
        const colorMap = {};
        groupAuras.forEach((color, group) => {
            colorMap[group] = color;
        });
        groupColors.value = colorMap;
    }

    groupNames.forEach((group, i) => {
        groupAuras.set(group, colors[group]);
    });


    // force simulation to control positioning
    const simulation = d3.forceSimulation(nodes.value)
        .force('charge', d3.forceManyBody().strength(d => -200 - Math.random() * 100))
        .force('center', d3.forceCenter(width / 2, height / 2))
        .force('collision', d3.forceCollide().radius(nodeRadius*1.1))
        // custom clustering force that pulls each node towards its' group center
        .force('cluster', forceCluster(0.4));

    // build the svg
    const svgElement = d3.select(svg.value);

    svgElement.append("defs").selectAll("clipPath")
        .data(nodes.value)
        .join("clipPath")
        .attr("id", d => `clip-${d.id}`)
        .append("circle")
        .attr("r", nodeRadius);

    // add circles to create rippling aura effect
    const rippleGroup = svgElement.append('g')
        .attr('class', 'ripples')

    const node = svgElement.append('g')
        .selectAll('a')
        .data(nodes.value)
        .join('a')
        .attr('xlink:href', d => d.url || null)
        .attr('target', '_blank')
        .append('circle')
        .attr('r', nodeRadius)
        .attr('stroke', d => groupAuras.get(d.group))
        .attr('stroke-width', 6)
        .style('fill', d => `url(#pattern-${d.id})`)
        .call(drag(simulation));

    // svg defs
    const defs = svgElement.append('defs');

    defs.append('filter')
        .attr('id', 'psychedelic-glow')
        .attr('x', '-50%')
        .attr('y', '-50%')
        .attr('width', '200%')
        .attr('height', '200%')
        .html(`
            <feGaussianBlur in="SourceGraphic" stdDeviation="5" result="blur"/>
            <feColorMatrix in="blur" mode="matrix"
                values="1 0 0 0 0
                        0 1 0 0 0
                        0 0 1 0 0
                        0 0 0 20 -10" result="goo"/>
            <feBlend in="SourceGraphic" in2="goo" />
        `);

    // define styles for images in bubbles
    const patterns = defs.append('defs')
        .selectAll('pattern')
        .data(nodes.value)
        .enter()
        .append('pattern')
        .attr('id', d => `pattern-${d.id}`)
        .attr('height', 1)
        .attr('width', 1)
        .attr('patternContentUnits', 'objectBoundingBox')

    // add profile images
    patterns.append('image')
        .attr('href', d => d.img)
        .attr('height', 1)
        .attr('width', 1)
        .style('opacity', 0.8)
        .attr('preserveAspectRatio', 'xMidYMid slice')
        .style('filter', 'grayscale(100%)'); // greyscale images

    // fill images same color as group
    patterns.append('rect')
        .attr('width', 1)
        .attr('height', 1)
        .attr('fill', d => groupAuras.get(d.group))
        .style('opacity', 0.1);

    // name labels for mouseover
    const labels = svgElement.append('g')
        .selectAll('text')
        .data(nodes.value)
        .join('text')
        .text(d => d.id)
        .attr('x', d => d.x)
        .attr('y', d => d.y - nodeRadius - 10)
        .attr('text-anchor', 'middle')
        .attr("dominant-baseline", "central")
        .style('visibility', 'hidden')
        .attr('pointer-events', 'none');

    //mouseover effects
    node.on('mouseover', (event, d) => {

        d3.select(event.currentTarget)
            .style('fill', d => groupAuras.get(d.group))
            .style('opacity', 0.8);

        labels.filter(ld => ld.id === d.id)
            .style('visibility', 'visible')
            .style('fill', 'black')
            .style('font-weight', '800')
            .style('stroke', 'white')
            .style('stroke-width', '0.1');

        createRippleEffect(d)

        })
        .on('mouseout', (event, d) => {

            d3.select(event.currentTarget)
                .style('fill', `url(#pattern-${d.id})`)
                .style('opacity', 1);

            labels.filter(ld => ld.id === d.id)
                .style('visibility', 'hidden');
        })
        .on('click', (event, d) => {
            window.open(d.url, '_blank');
        });

    // allow circles to move
    simulation.on('tick', () => {
        
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

    // allow dragging of circles
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

    // but dont drag outside the container
    function constrain(value, min, max) {
        return Math.max(min+10, Math.min(max-10, value));
    }

    function forceCluster(strength = 0.1) {
        return alpha => {
            nodes.value.forEach(d => {
                // get the target center for the circle's group
                const center = groupCenters.get(d.group);

                // find the distance between the circle and the center
                const dx = center.x - d.x;
                const dy = center.y - d.y;

                // adjust the force so the circle is pulled towards the group center
                d.vx += dx * strength * alpha;
                d.vy += dy * strength * alpha;
            });
        };
    }
    function createRippleEffect(d) {
        const rippleCount = 1;
        const duration = 1000;
        const rippleRadius = nodeRadius * 2;

        for (let i = 0; i < rippleCount; i++) {
            rippleGroup.append('circle')
                .attr('cx', d.x)
                .attr('cy', d.y)
                .attr('r', 0)
                .attr('fill', 'none')
                .attr('stroke', groupAuras.get(d.group))
                .attr('stroke-width', 9)
                .attr('opacity', 0.8)
                .attr('filter', 'url(#psychedelic-glow)')
                .transition()
                .delay((i-1) * 600)
                .duration(duration)
                .ease(d3.easeSinInOut)
                .attr('r', rippleRadius)
                .attr('opacity', 0)
                .remove();
        }
    }

    updateGroupColors();

}

</script>

<style lang="scss">
.svg-container {
    display: flex;
    position: relative;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 60vh;
}
svg {
  width: 100%;
  height: 100%;
  overflow: visible;
  display: block;
}
</style>

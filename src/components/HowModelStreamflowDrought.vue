<template>
  <section>
    <div
      class="text-container"
      id="how-model-section"
    >
      <h2
        class="section-title"
      >
        <span>
          {{ text.title }}
        </span>
      </h2>
      <p
        class="section-subtitle"
        v-html="text.subtitle"
      />
      <p v-html="text.paragraph1" />
      <p v-html="text.paragraph2" />
      <p v-html="text.paragraph3" />
      <p v-html="text.paragraph4" />
    </div>
  </section>
</template>

<script setup>
  import { onMounted } from "vue";
  import { useWindowSizeStore } from '@/stores/WindowSizeStore';

  // define props
  defineProps({
    text: {  
      type: Object,
      default: () => ({})
    }
  })

  // global variables
  const windowSizeStore = useWindowSizeStore();

  onMounted(() => {
    // re-position tooltips that go off screen
    positionTooltips('how-model-section')
  })

  function positionTooltips(id) {
    // get all tooltips in specified container
    const container = document.querySelector(`#${id}`)
    let refTooltips = container.querySelectorAll(".tooltip-group");
    refTooltips.forEach(tooltip => positionTooltip(tooltip)); 
  }

  function positionTooltip(tooltip_group) {
    // Get .tooltiptext sibling
    const tooltip = tooltip_group.querySelector(".tooltiptext");
    
    // Get calculated tooltip coordinates and size
    let tooltip_rect = tooltip.getBoundingClientRect();

    // Corrections if out of window to left
    if (tooltip_rect.x < 0) {
      // reset left position and drop transformation
      tooltip.classList.add('tooltip-left')
    }    
    // Corrections if out of window to right
    tooltip_rect = tooltip.getBoundingClientRect();
    if ((tooltip_rect.x + tooltip_rect.width) > windowSizeStore.windowWidth*0.95) {
      // reset tooltip width, with some buffer room
      document.getElementById(tooltip.id).style.width = (windowSizeStore.windowWidth - tooltip_rect.x)*0.8 + "px";
    }
  }
</script>

<style lang="scss">
</style>
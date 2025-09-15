<template>
  <section>
    <div
      class="text-container"
    >
      <h3 v-html="text.heading" />
      <p v-html="text.paragraph1" />
      <div
        class="explainer-image-container"
      >
        <img
          :src="getImageURL(text.figurePath)"
          class="explainer-image"
          :alt="text.figureAlt"
        >
      </div>
      <p v-html="text.paragraph2" />
    </div>
  </section>
</template>

<script setup>
  // define props
  defineProps({
    text: {  
      type: Object,
      default: () => ({})
    }
  })

  function getImageURL(file) {
    return new URL(`../assets/images/${file}`, import.meta.url).href
  }
</script>

<style scoped>
.explainer-image-container {
  text-align: center;
}
.explainer-image {
  padding: 10px;
  max-width: 95%;
}
</style>
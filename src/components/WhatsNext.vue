<template>
  <section>
    <div
      class="text-container"
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
      <h3 v-html="text.headingA" />
      <p v-html="text.paragraphA1" />
      <h3 v-html="text.headingB" />
      <p v-html="text.paragraphB1" />
      <h3 v-html="text.headingC" />
      <p v-html="text.paragraphC1" />
      <h3 v-html="text.headingD" />
      <p v-html="text.paragraphD1" />
      <div
        class="explainer-image-container"
      >
        <img
          :src="getImageURL(text.figureDpath)"
          class="explainer-image"
        >
      </div>
      <h3 v-html="text.headingE" />
      <p v-html="text.paragraphE1" />
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
  max-width: 85%;
  @media only screen and (max-width: 600px) {
    max-width: 100%;
  }
}
</style>
<style lang="scss">
#baseflow-tooltip {
  margin-left: -330px;
}
</style>
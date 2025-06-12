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
      <p v-html="text.paragraph1" />
      <p v-html="text.paragraph2" />
      <p v-html="text.paragraph3" />
      <p v-html="text.paragraph4" />
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
</script>

<style lang="scss">
#characteristics-tooltip {
  margin-left: -240px;
}
</style>
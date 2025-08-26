<template>
  <ObservationExplore
    :text="text.observationExplore"
  />
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
      <MapperDiagram
        :text="text.mapperDiagram"
      />
    </div>
  </section>
</template>

<script setup>
  import ObservationExplore from '@/components/ObservationExplore.vue';
  import MapperDiagram from '@/components/MapperDiagram.vue';

  // define props
  defineProps({
    text: {  
      type: Object,
      default: () => ({})
    }
  })

</script>

<style scoped>
.mapper-image-container {
  text-align: center;
}
.mapper-image {
  padding: 10px;
  max-width: 85%;
  @media only screen and (max-width: 600px) {
    max-width: 100%;
  }
}
</style>
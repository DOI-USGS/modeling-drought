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
    </div>
    <AboutTheTeam 
      :text="text.aboutTheTeam"
    />
  </section>
</template>

<script setup>
  import AboutTheTeam from '@/components/AboutTheTeam.vue';

  // define props
  defineProps({
    text: {  
      type: Object,
      default: () => ({})
    }
  })
</script>

<style>
</style>
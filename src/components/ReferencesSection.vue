<template>
  <VizSection
    id="references"
    :figures="false"
    :fig-caption="false"
  >
    <!-- HEADING -->
    <template 
      v-if="references.title"
      #heading
    >
      <h1
        v-if="titleLevel === '1'"
        v-html="references.title"
      />
      <h2
        v-if="titleLevel === '2'"
        v-html="references.title"
      />
      <h3
        v-if="titleLevel === '3'"
        v-html="references.title"
      />
      <span
        v-else
        v-html="references.title"
      />
    </template>
    <template #aboveExplanation>
      <div
        id="references-container"
      >
        <div
          v-for="reference in references.references"
          :key="reference.num"
        >
          <p>
            <span v-html="reference.num" />. <span v-html="reference.authors" /> (<span v-html="reference.year" />). <a
              :href="reference.link"
              target="_blank"
            ><span v-html="reference.title" /></a>
            <span v-if="reference.data_release">: U.S. Geological Survey data release</span>.
            <span v-if="reference.journal">
              <span
                class="journal-name"
                v-html="reference.journal_name"
              />
              <span v-if="reference.journal_issue">, {{ reference.journal_issue }}</span>.
            </span>
            <span
              v-if="reference.doi"
              v-html="reference.doi"
            />
            <span
              v-else
              v-html="reference.link"
            />
          </p>
        </div>
      </div>
    </template>
  </VizSection>
</template>

<script setup>
  import VizSection from '@/components/VizSection.vue';

  // define props
  defineProps({
    titleLevel: {
      type: String,
      default: ""
    },
    references: {
      type: Object,
      // Object or array defaults must be returned from
      // a factory function.
      default() {
        return {
          title: "References",
          references: []
        }
      }
    },
  })
</script>

<style scoped lang="scss">
  #references-container span {
    /* These are technically the same, but use both */
    overflow-wrap: break-word;
    word-wrap: break-word;

    -ms-word-break: break-all;
    /* This is the dangerous one in WebKit, as it breaks things wherever */
    word-break: break-all;
    /* Instead use this non-standard one: */
    word-break: break-word;

    /* Adds a hyphen where the word breaks, if supported (No Blink) */
    -ms-hyphens: auto;
    -moz-hyphens: auto;
    -webkit-hyphens: auto;
    hyphens: auto;
  }
  .journal-name {
    font-style: italic;
  }
</style>
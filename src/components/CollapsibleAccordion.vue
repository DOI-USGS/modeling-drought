<template>
  <div 
    class="accordion-container"
    :style="{'border-left-color': leftBorderColor }"
  > 
    <button 
      class="accordion" 
      :class="{ active: active }" 
      :style="{'background-color': active ? buttonActiveBackgroundColor : buttonInactiveBackgroundColor, 'font-weight': buttonFontWeight, color: buttonFontColor}"
      @click="accordionClick"
    >
      <p 
        class="accordion-button-text" 
        v-html="heading" 
      />
      <span 
        class="accordion-button-text symbol"
      />
    </button>
    <div 
      class="panel" 
      :class="[{ 'active': active }]"
    >
      <div
        v-for="item, index in content"
        :key="index"
      >
        <p
          v-if="item.type=='text'"
          v-html="item.content"
        />
        <p
          v-if="item.type=='quote'"
          class="quote"
          v-html="item.content"
        />
        <div
          v-if="item.type=='image'"
          class="accordion-image-container"
        >
          <img
            :src="getImageURL(item.content)"
            class="accordion-image"
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref } from "vue";

  const props = defineProps({
    activeOnLoad: Boolean, // should accordion be open on load
    heading: {
      type: String,
      required: true,
      default: 'Accordion heading'
    },
    content: {
      type: Array,
      required: true,
      default: () => ([
        {
          type: 'text',
          content: 'Accordion content'
        }
      ]),
    },
    leftBorderColor: {
      type: String,
      required: true,
      default: '#000000'
    },
    buttonActiveBackgroundColor: {
      type: String,
      required: true,
      default: '#F2F2F2'
    },
    buttonInactiveBackgroundColor: {
      type: String,
      required: true,
      default: '#ffffff'
    },
    buttonFontWeight: {
      type: String,
      required: true,
      default: '800'
    },
    buttonFontColor: {
      type: String,
      required: true,
      default: '#000000'
    }
  })

  const active = ref(props.activeOnLoad);

  function accordionClick() {
    active.value = !active.value;
  }

  function getImageURL(file) {
    return new URL(`../assets/images/${file}`, import.meta.url).href
  }
</script>

<style scoped lang="scss">
$margin: 10px;
$padding: 10px;
$left-border-width: 5px;
.accordion-container {
  border-left: $left-border-width solid;  
  border-right: 1px solid #dee2e6;
  border-top: 1px solid #dee2e6;
  border-bottom: 1px solid #dee2e6;
  border-radius: .25rem;
  overflow-wrap: break-word;
  margin: $margin calc(($margin + $left-border-width/2)*-1) $margin calc(($margin + $left-border-width/2)*-1);
  overflow: hidden;
}
.accordion {
  cursor: pointer;
  padding: calc($padding / 2);
  padding-left: $padding;
  width: 100%;
  border: none;
  text-align: left;
  outline: none;
  transition: 0.4s;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  border-radius: 0 .25rem .25rem 0;
}
.accordion::before{
  content: "";
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  border: 2px solid transparent;
  z-index: -1;
  transition: border-color 0.3s;
}
.accordion span::before {
  content: "\1F7A1";
}
.accordion.active span::before {
  display: block;
  content: "\1F7A1";
  transform: rotate(45deg);
}
/* .accordion:hover::before, .accordion.active::before {
  border-color: var(--usgs-blue);
} */
// .active, .accordion:hover {
//   color: var(--color-title-text);
// }
.accordion:hover {
  background-color: var(--medium-light-grey) !important;
}
.accordion-button-text {
  padding: 0;
}
.panel {
  display: none; 
}
.panel.active {
  display: block; 
}
.panel p {
  margin: $margin 0 $margin 0;
  padding: $padding;
}
.symbol {
  font-size: 3rem;
  font-weight: bold;
  padding-right: calc($padding / 2);
}
.accordion-image-container {
  text-align: center;
}
.accordion-image {
  padding: 10px;
  max-width: 95%;
}
.quote {
  font-style: italic;
  padding-left: calc($padding * 2) !important;
  opacity: 0.7;
}
ul {
  display: list-item;
  padding-bottom: 1rem;
  padding-left: 0.25rem;
  margin-left: 40px;
}
ul:first-child {
  padding-top: 1rem;
}
ul:last-child {
  padding-bottom: 1rem;
}
</style>
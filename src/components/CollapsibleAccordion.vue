<template>
  <div 
    :id="accordionId"
    class="accordion-container"
    :style="{'border-left-color': leftBorderColor }"
  > 
    <button 
      class="accordion" 
      type="button"
      :id="`${accordionId}-button`"
      :class="{ active: active }" 
      :aria-expanded="active ? true : false"
      :aria-controls="`${accordionId}-panel`"
      :style="{'background-color': active ? buttonActiveBackgroundColor : buttonInactiveBackgroundColor, 'font-weight': buttonFontWeight, color: buttonFontColor}"
      @click="accordionClick"
    >
      <p 
        class="accordion-button-text" 
        v-html="heading" 
      />
      <span 
        class="accordion-button-text symbol"
        :class="{ active: active }"
      >
        <svg 
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
        >
          <line 
            class="symbol-line"
            x1="10"
            y1="1"
            x2="10"
            y2="19"
            :stroke="buttonFontColor"
          />
          <line
            class="symbol-line"
            x1="19"
            y1="10"
            x2="1"
            y2="10"
            :stroke="buttonFontColor"
          />
        </svg>  
      </span>
    </button>
    <div 
      role="region"
      class="panel" 
      :aria-labelledby="`${accordionId}-button`"
      :id="`${accordionId}-panel`"
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
            :class="{ mobile: mobileView}"
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref } from "vue";
  import { isMobile } from 'mobile-device-detect';

  const props = defineProps({
    activeOnLoad: Boolean, // should accordion be open on load
    accordionId: {
      type: String,
      required: true,
      default: ""
    },
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

  // global variables
  const mobileView = isMobile;
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
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  border-radius: 0 .25rem .25rem 0;
}
.accordion:focus-visible {
  border: 2px solid;
  border-radius: 0 .25rem .25rem 0;
}
.accordion:hover {
  background-color: var(--medium-light-grey) !important;
}
.accordion-button-text {
  padding: 0;
}
.symbol {
  height: 35px;
  display: flex;
  align-items: center;
  padding-right: calc($padding / 2);
}
.symbol svg {
  width: 25px;
  height: 25px;
}
.symbol.active svg {
  transform: rotate(45deg);
}
.symbol-line {
  stroke-width: 0.8px;
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
.accordion-image-container {
  text-align: center;
}
.accordion-image {
  padding: 10px;
  max-width: 95%;
}
.accordion-image.mobile {
  padding: 10px;
  max-width: 100%;
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
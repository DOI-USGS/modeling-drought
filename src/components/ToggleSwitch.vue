<template>
  <div class="checkbox_wrap toggle-container" aria-label="Toggle container">
    <label class="toggle-label" aria-hidden="true">
      <!-- Left label for either/or use case -->
      <span 
        v-if="leftLabel" 
        class="toggle-text" 
        :class="{ tactive: !modelValue }" 
        aria-hidden="true"
      >
        {{ leftLabel }}
      </span>
      
      <!-- Toggle switch -->
      <input 
        type="checkbox" 
        class="toggle-input" 
        :checked="modelValue"
        @change="$emit('update:modelValue', !modelValue)" 
        aria-hidden="true"
      />
      <span 
       class="toggle-slider"
       :style="{ backgroundColor: modelValue ? rightColor : leftColor }"
        aria-hidden="true"
       ></span>

      <!-- Right label for either/or use case or single toggle label -->
      <span 
        v-if="rightLabel" 
        class="toggle-text" 
        :class="{ tactive: modelValue, inactive: !modelValue }"
        aria-hidden="true"      >
      {{ rightLabel }}
    </span>
     <!-- Single label -->
     <span 
        v-else-if="label" 
        class="toggle-text"
        :class="{ tactive: modelValue, inactive: !modelValue }"
        aria-hidden="true"
      >
        {{ label }}
      </span>
    </label>
  </div>
</template>

<script setup>
defineProps({
  modelValue: Boolean, // v-model binding for toggle state

  // optional props for either/or labels
  leftLabel: {
    type: String,
    required: false
  },
  rightLabel: {
    type: String,
    required: false
  },

  // optional prop for single label (on/off use case)
  label: {
    type: String,
    required: false
  },
  // colors for each label and inactive state
  leftColor: {
    type: String,
    default: 'var(--inactive-grey)' 
  },
  rightColor: {
    type: String,
    default: 'var(--soft-black)' 
  },
  inactiveColor: {
    type: String,
    default: 'var(--inactive-grey)' 
  }
});

defineEmits(['update:modelValue']);
</script>

<style scoped>

.toggle-container {
  display: flex;
  align-items: start;
  gap: 10px;
}

/* toggle label for positioning */
.toggle-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  position: relative;
}

/* text styles */
.toggle-text {
  transition: color 0.3s ease;
  color: var(--inactive-text-grey);
}

.toggle-text.tactive {
  color: var(--black-soft); /* active label is black */
}
.toggle-input:focus-visible {
  outline: none; /* removes focus outline */
}

.toggle-label:focus-visible {
  outline: none; /* removes focus outline */
}

/* toggle input (hidden) */
.toggle-input {
  display: none;
}

/* toggle slider styles */
.toggle-slider {
  flex-shrink: 0;
  position: relative;
  width: 40px;
  height: 20px;
  border-radius: 20px;
  transition: background-color 0.3s ease;
  border: 1px solid var(--black-soft);
}

.toggle-slider::before {
  content: "";
  position: absolute;
  width: 16px;
  height: 16px;
  background-color: white;
  border-radius: 50%;
  top: 1.5px;
  left: 1.5px;
  transition: transform 0.3s ease;
  border: 1px solid var(--black-soft); 
}

/* move slider to the right when checked */
.toggle-input:checked + .toggle-slider::before {
  transform: translateX(20px);
  border: 1px solid var(--black-soft); 
}

</style>

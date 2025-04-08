<template>
  <div class="radio_wrap">
    <label
      v-for="option in options"
      :key="option.value"
      class="radio-label"
      :class="{ selected: modelValue === option.value }"
      :style="{
        backgroundColor: modelValue === option.value
          ? `${option.color}0D` || `${activecolor}0D` // 20 is ~12% opacity in hex
          : 'transparent'
      }"
    >
      <input
        type="radio"
        class="radio-input"
        :value="option.value"
        :checked="modelValue === option.value"
        name="radio-group"
        @change="$emit('update:modelValue', option.value)"
      >
      <span
        class="radio-button"
        :style="{
          borderColor: modelValue === option.value ? option.color || activecolor : inactivecolor,
          backgroundColor: modelValue === option.value ? option.color || activecolor : 'transparent'
        }"
      />
      <span
        class="radio-check"
        :style="{
          backgroundColor: modelValue === option.value ? centercolor : 'transparent'
        }"
      />
      <span
        class="radio-text"
        :class="{ ractive: modelValue === option.value }"
      >
        {{ option.label }}
      </span>
    </label>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    default: ''
  }, // v-model binding for selected value

  // array of radio options: [{ label: 'Option 1', value: 'opt1' }, ...]
  options: {
    type: Array,
    required: true
  },

  // optional colors
  activecolor: {
    type: String,
    default: 'var(--black-soft)'
  },
  inactivecolor: {
    type: String,
    default: 'var(--inactive-grey)'
  },
  centercolor: {
    type: String,
    default: 'var(--black-soft)'
  },
});

defineEmits(['update:modelValue']);
</script>

<style scoped>
.radio_wrap {
  /* display: flex; */
  row-gap: 2px;
  column-gap: 16px;
  flex-wrap: wrap;
}

.radio-label {
  display: flex;
  width: max-content;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  user-select: none;
  padding: 6px 10px;
}
.radio-label.selected {
  background-color: rgba(0, 0, 0, 0.05); /* or use a theme color */
  border-radius: 8px;
  transition: background-color 0.3s ease;
}


.radio-input {
  display: none;
}

.radio-button {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  border: 2px solid;
  position: relative;
  transition: border-color 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.radio-check {
  position: absolute;
  transform: translate(4px,0);
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.radio-text {
  color: var(--inactive-text-grey);
  transition: color 0.3s ease;
}

.radio-text.ractive {
  color: var(--black-soft);
}
</style>

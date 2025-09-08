<template>
  <ion-button
    :class="customClass"
    :disabled="disabled"
    :expand="expand"
    :color="theme"
    fill="solid"
    @click="$emit('click')"
  >
    <slot name="prefix" />
    <slot />
  </ion-button>
</template>

<script setup>
defineProps({
  customClass: String,
  theme: { type: String, default: "primary" },
  expand: { type: String, default: "block" },
  disabled: Boolean,
});
</script>

<template>
  <svg :width="size" :height="size" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M30 40H20C18.8954 40 18 40.8954 18 42V82C18 83.1046 18.8954 84 20 84H30C31.1046 84 32 83.1046 32 82V42C32 40.8954 31.1046 40 30 40Z" fill="currentColor"/>
    <path d="M82 40H60L63 25C63.5 22 63.5 20 62.5 18C61.5 16 60 15 58 15H55C53.5 15 52 15.5 51 16.5L32 40V84H72C76 84 79.5 81 80 77L84 47C84.5 44.5 83.5 42 82 40ZM72 77H39V47L54 28.5C54.5 27.5 55 25.5 55 24V22L58 22.5L54 44H82L78 74C77.5 75.5 76 77 72 77Z" fill="currentColor"/>
  </svg>
</template>

<script setup>
const props = defineProps({
  size: {
    type: Number,
    default: 45
  }
})
</script>
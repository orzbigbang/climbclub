<script setup>
import { useTemplateRef, onMounted, onBeforeUnmount } from 'vue';
import BIRDS from 'vanta/dist/vanta.birds.min'
import DOTS from 'vanta/dist/vanta.dots.min'

const emit = defineEmits(['loaded'])

const vantaRef = useTemplateRef("vantaRef")
let vantaEffect = null

onMounted(() => {
  vantaEffect = BIRDS({
    el: vantaRef.value,
    backgroundColor: "#222",
    mouseControls: true,
    touchControls: true,
    gyroControls: false,
    minHeight: 200.00,
    minWidth: 200.00,
    scale: 1.00,
    scaleMobile: 1.00
  })
//   vantaEffect = DOTS({
//   el: vantaRef.value,
//   backgroundColor: "#222",
//   mouseControls: true,
//   touchControls: true,
//   gyroControls: false,
//   minHeight: 200.00,
//   minWidth: 200.00,
//   scale: 1.00,
//   scaleMobile: 1.00 
// })
  emit('loaded')
})

onBeforeUnmount(() => {
  if (vantaEffect) {
    vantaEffect.destroy()
  }
})
</script>

<template>
<div class="main-bg" ref='vantaRef'>
  <slot></slot>
</div>
</template>

<style lang='less' scoped>
.main-bg {
  width: 100%;
  height: 80vh;
  padding: 30px;
  color: white;
}
</style>
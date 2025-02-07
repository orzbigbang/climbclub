<script setup>
import Scene1TextSplit from './Scene1TextSplit.vue'
import Scene2HorizontalScroll from './Scene2HorizontalScroll.vue'
import Scene3Zoom from './Scene3Zoom.vue'
import Scene4Moving from './Scene4Moving.vue'

import { onMounted, onBeforeUnmount, ref } from 'vue';
import Lenis from 'lenis'

let lenis = null
let gsapContext = null

const scene1 = ref(null)
const scene2 = ref(null)
const scene3 = ref(null)
const scene4 = ref(null)

const emit = defineEmits(['loaded'])

onMounted(async () => {
  // TODO move all of these to App.vue
  try {
    await Promise.all([
      // 等待必要资源加载
      document.fonts.ready,

      // 等待场景组件加载和至少2秒延迟
      scene1.value.$el.complete,
      scene2.value.$el.complete,
      scene3.value.$el.complete,
      scene4.value.$el.complete,
    ])
  } finally {
    emit('loaded')
  }
  
  
  // Initialize a new Lenis instance for smooth scrolling
  // Use requestAnimationFrame to continuously update the scroll
  lenis = new Lenis();
  const raf = (time) => {
    lenis.raf(time);
    requestAnimationFrame(raf);
  }
  requestAnimationFrame(raf);

  gsap.registerPlugin(ScrollTrigger)
  // gsap.registerPlugin(ScrambleTextPlugin)
  
  gsap.config({
    force3D: true
  });
  
  gsapContext = gsap.context(() => {
    // scene-1 - reveal text
    scene1.value.scene1Gsap()

    // scene-2 - horizontal scrolling
    scene2.value.scene2Gsap()

    // scene-3 - zoomin and flip to scene-4(last)
    scene3.value.scene3Gsap()

    // scene-4 - moving
    scene4.value.scene4Gsap()
  })
})

onBeforeUnmount(() => {
  if (lenis) lenis.destroy()
  if (gsapContext) gsapContext.revert()
})

</script>

<template>
  <Scene1TextSplit ref="scene1"/>
  <Scene2HorizontalScroll  ref="scene2"/>
  <Scene3Zoom  ref="scene3"/>
  <Scene4Moving  ref="scene4"/>
</template>

<style lang='less'>

</style>
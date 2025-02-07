<script setup>
const scene4Gsap = () => {
  
}

defineExpose({
  scene4Gsap
})
</script>

<template>
  <section class="section-wrapper scene-4 pos-rel z-100">
    <div class="wrapper flex-center">
      <h2>Welcome to the Hiking Club</h2>
    </div>
  </section>
</template>

<style scoped lang='less'>
@scene4-color: #ff6347;

.scene-4 {
  width: 100vw;
  height: 100vh;
  background-color: @scene4-color;
  display: none;
}

.wrapper {
  min-height: 100vh;
}
</style>
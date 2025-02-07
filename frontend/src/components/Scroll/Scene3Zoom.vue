<script setup>
const scene3Gsap = () => {
  const transitionText = document.querySelector(".scene-3 .transition-text");
  const transitionX = document.querySelector(".scene-3 .transition-text .zoom-in-word");
  const nextScene = document.querySelector(".scene-4");
  const scrollIndicator = document.querySelector(".scroll-indicator")
  const scene3TL = gsap.timeline({
    scrollTrigger: {
      trigger: transitionText,
      start: 'top 30%',
      end: 'top -20%',
      pin: true,
      scrub: true,
    },
  });
  scene3TL.to(
    transitionText, 
    {
      scale: 15,
    },
  ).to(
    transitionX, 
    {
      scale: 2.4,
    }
  ).to(
    transitionX,
    {
      y: -200,
      scale: 22,
    },
  ).to(
    nextScene,
    {
      display: "block",
      position: "fixed",
      top: "0",
      left: "0"
    }
  ).to(
    scrollIndicator,
    {
      opacity: 0
    },
    "<"
  ).to(
    transitionX,
    {
      scale: 1,
    },
  )
}

defineExpose({
  scene3Gsap
})
</script>

<template>
  <section class="section-wrapper scene-3 paper-feel-bg">
    <div class="transition-wrapper wrapper flex-center pos-rel">
      <h2 class="transition-text z-1">Go E<div class="zoom-in-word">x</div>plore</h2>
    </div>
  </section>
</template>

<style scoped  lang='less'>
@text-size: 64px;
@scene4-color: #ff6347;

.paper-feel-bg {
  background: 
    linear-gradient(135deg, rgba(255, 255, 255, 1), rgba(240, 240, 240, 1)), /* 渐变底色 */
    radial-gradient(rgba(0, 0, 0, 0.05), transparent 70%), /* 噪点图案 */
    radial-gradient(rgba(0, 0, 0, 0.1), transparent 50%) /* 额外层次感 */;
  background-blend-mode: overlay, overlay;
  background-size: 100% 100%, 8px 8px, 5px 5px; /* 第二、三层噪点密度调整 */
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.1); /* 添加内阴影增强纸感 */
}

.scene-3 {
  .transition-text {
    font-size: @text-size;
    transform-origin: center center;
    will-change: transform;
  
    .zoom-in-word {
      display: inline-block;
      color: @scene4-color;
    }
  }

  &::after {
    &:extend(.paper-feel-bg);
    content: "";
    display: block;
    height: 70vh;
  }
}

.wrapper {
  min-height: 100vh;
}
</style>
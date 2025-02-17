<script setup>
import { ref } from 'vue';

const minHeight = ref(800)
const scrollWidth = ref(minHeight.value * 7.1)

const scene2Gsap = () => {
  const shapes = document.querySelectorAll(".scene-2 .shape")
  const fundamental_size = 1400

  // 创建时间轴来控制两段动画
  shapes.forEach((shape, i) => {
    // 第一段：元素分散
    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: shape,
        start: "top 25%",
        end: `top -${minHeight.value * 0.88}%`,
        scrub: true,
        pin: true,
      }
    });
    
    tl.to(shape, {
      transform: `translateX(${fundamental_size * i + (fundamental_size / 2)}px)`,
    });

    // 第二段：整体向左滚动
    tl.fromTo(shape, {
      transform: `translateX(${fundamental_size * i + (fundamental_size / 2)}px)`,
    }, {
      x: `-=${scrollWidth.value}`,
    });
  });
}

defineExpose({
  scene2Gsap
})
</script>

<template>
  <section class="section-wrapper scene-2">
    <div class="h-scroll-wrapper">
      <div class="show-box-wrapper">
        <img class="shape pos-abs" v-for="i in 5" :key="i">
        <!-- <img class="shape pos-abs" v-for="i in 5" :key="i" :src="`/${i}.jpg`" loading="lazy"> -->
      </div>
    </div>
  </section>
</template>

<style scoped  lang='less'>
@base: 16px;

.scene-2 {
  // @colors: 
  // linear-gradient(135deg, #ff9a9e, #fad0c4), 
  // linear-gradient(135deg, #a1c4fd, #c2e9fb), 
  // linear-gradient(135deg, #fbc2eb, #a6c1ee), 
  // linear-gradient(135deg, #ff9966, #ff5e62), 
  // linear-gradient(135deg, #141e30, #527dae);

  min-height: calc(v-bind('minHeight') * 1vh);
  padding: 2 * @base;
  background-image: linear-gradient(135deg, #ff5e62, #ff9966);

  .h-scroll-wrapper {
    
    .show-box-wrapper {

      .shape {
        width: 20 * @base;
        height: 30 * @base;
        border-radius: @base;
        // background-image: url(1.jpg);
        background-size: cover;
        // background: linear-gradient(135deg, #141e30, #527dae);
        will-change: transform;
      }
    }
  }
}
</style>
<script setup>
import { onMounted, onBeforeUnmount, ref } from 'vue';
import Lenis from 'lenis'
// import { SplitText } from "gsap-trial/SplitText";
// import { ScrambleTextPlugin } from "gsap-trial/ScrambleTextPlugin";

import ScrollArrow from '@/components/ScrollArrow.vue';

let lenis = null
let gsapContext = null

const isLoading = ref(true)

onMounted(async () => {
  try {
    await Promise.all([
      // 等待必要资源加载
      document.fonts.ready,
      // 可以添加其他需要等待的资源
    ])
  } finally {
    isLoading.value = false
  }
  
  // Initialize a new Lenis instance for smooth scrolling
  lenis = new Lenis();

  // Use requestAnimationFrame to continuously update the scroll
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
    const splitTypes = document.querySelectorAll(".reveal-type")
    splitTypes.forEach((sentenceDOM, i) => {
      const text = new SplitType(sentenceDOM, {types: 'words,chars', whitespace: 'preserve'})
      
      gsap.from(text.chars, {
          scrollTrigger: {
            trigger: sentenceDOM,
            start: 'top 80%',
            end: 'top 30%',
            scrub: true,
          },
          opacity: 0.2,
          stagger: 0.2
        })
    })

    // scene-2 - horizontal scrolling
    const shapes = document.querySelectorAll(".scene-2 .shape")
    const shapesWrapper = document.querySelector(".scene-2 .show-box-wrapper")
    const fundamental_size = 1400

    // 创建时间轴来控制两段动画
    shapes.forEach((shape, i) => {
      // 第一段：元素分散
      const tl = gsap.timeline({
        scrollTrigger: {
          trigger: shape,
          start: "top 30%",
          end: "top -500%",
          scrub: true,
          pin: true,
          // markers: true,
        }
      });
      
      tl.to(shape, {
        transform: `translateX(${fundamental_size * i + (fundamental_size / 2)}px)`,
      });

      // 第二段：整体向左滚动
      tl.fromTo(shape, {
        transform: `translateX(${fundamental_size * i + (fundamental_size / 2)}px)`,
      }, {
        transform: `translateX(${-fundamental_size}px)`,
      });
    });

    // scene-3 - zoomin and flip to scene-4(last)
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
  })
})

onBeforeUnmount(() => {
  if (lenis) lenis.destroy()
  if (gsapContext) gsapContext.revert()
})


import {getRandomSentences, getRandomColors} from '@/compositions/randomThing.js'
const randomSentences = getRandomSentences()
const randomColors = getRandomColors()
</script>

<template>
  <div v-if="isLoading" class="loading-overlay">
    <div class="loading-spinner"></div>
  </div>
  
  <ScrollArrow/>

  <section class="section-wrapper scene-1">
    <div class="type-wrapper flex-center" v-for="sentence, index in randomSentences" :style="{ backgroundColor: randomColors[index] }">
      <div class="reveal-type">{{ sentence }}</div>
    </div>
  </section>

  <section class="section-wrapper scene-2">
    <div class="h-scroll-wrapper">
      <div class="show-box-wrapper">
        <div class="shape pos-abs" v-for="_ in 5"></div>
      </div>
    </div>
  </section>

  <section class="section-wrapper scene-3 paper-feel-bg">
    <div class="transition-wrapper wrapper flex-center pos-rel">
      <h2 class="transition-text z-1">Go E<div class="zoom-in-word">x</div>plore</h2>
    </div>
  </section>

  <section class="section-wrapper scene-4 pos-rel z-100">
    <div class="wrapper flex-center">
      <h2>Welcome to the Climb Club</h2>
    </div>
  </section>
</template>

<style lang='less' scoped>
@scene4-color: #ff6347;

.wrapper {
  min-height: 100vh;
}

.paper-feel-bg {
  background: 
    linear-gradient(135deg, rgba(255, 255, 255, 1), rgba(240, 240, 240, 1)), /* 渐变底色 */
    radial-gradient(rgba(0, 0, 0, 0.05), transparent 70%), /* 噪点图案 */
    radial-gradient(rgba(0, 0, 0, 0.1), transparent 50%) /* 额外层次感 */;
  background-blend-mode: overlay, overlay;
  background-size: 100% 100%, 8px 8px, 5px 5px; /* 第二、三层噪点密度调整 */
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.1); /* 添加内阴影增强纸感 */
}

.scene-1 {
  @text-size: 32px;
  .type-wrapper {
    height: 70vh;
    width: 100vw;
    padding: 0 15%;
    margin: 0 auto;
  
    .reveal-type {
      width: 100%;
      font-size: @text-size;
      font-weight: bold;
      text-align: center;
    }
  }
}

.scene-2 {
  @base: 16px;
  @colors: 
  linear-gradient(135deg, #ff9a9e, #fad0c4), 
  linear-gradient(135deg, #a1c4fd, #c2e9fb), 
  linear-gradient(135deg, #fbc2eb, #a6c1ee), 
  linear-gradient(135deg, #ff9966, #ff5e62), 
  linear-gradient(135deg, #141e30, #527dae);

  min-height: 500vh;
  padding: 2 * @base;

  .h-scroll-wrapper {
    
    .show-box-wrapper {
      background-color: linear-gradient(135deg, #fbc2eb, #a6c1ee);
      .shape {
        width: 20 * @base;
        height: 30 * @base;
        border-radius: @base;
        background: linear-gradient(135deg, #141e30, #527dae);
        will-change: transform;
      }
    }
  }
}

.scene-3 {
  @text-size: 64px;
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

.scene-4 {
  @text-size: 32px;

  width: 100vw;
  height: 100vh;
  background-color: @scene4-color;
  display: none;
}
</style>
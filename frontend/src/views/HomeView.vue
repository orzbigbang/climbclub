<script setup>
import {useScroll} from '@/compositions/scroll.js'
useScroll()

import {getRandomSentences, getRandomColors} from '@/compositions/randomThing.js'
const randomSentences = getRandomSentences()
const randomColors = getRandomColors()
</script>

<template>
  <section class="section-wrapper scene-0">
    <div class="type-wrapper flex-center" v-for="sentence, index in randomSentences" :style="{ backgroundColor: randomColors[index] }">
      <div class="reveal-type">{{ sentence }}</div>
    </div>
  </section>

  <section class="section-wrapper scene-1 paper-feel-bg">
    <div class="transition-wrapper wrapper flex-center pos-rel">
      <h2 class="transition-text z-1">Go E<div class="zoom-in-word">x</div>plore</h2>
    </div>
  </section>

  <section class="section-wrapper scene-2 pos-rel z-100">
    <div class="wrapper flex-center">
      <h2>Welcome to the Climb Club</h2>
    </div>
  </section>
</template>

<style lang='less' scoped>
@scene2-color: #ff6347;

.wrapper {
  min-height: 100vh;
}

.scene-0 {
  .type-wrapper {
    height: 70vh;
    width: 100vw;
    padding: 0 15%;
    margin: 0 auto;
  
    .reveal-type {
      width: 100%;
      font-size: 36px;
      font-weight: bold;
      text-align: center;
    }
  }
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
  .transition-text {
    font-size: 64px;
    transform-origin: center center;
  
    .zoom-in-word {
      display: inline-block;
      color: @scene2-color;
    }
  }

  &::after {
    &:extend(.paper-feel-bg);
    content: "";
    display: block;
    height: 70vh;
  }
}

.scene-2 {
  width: 100vw;
  height: 100vh;
  background-color: @scene2-color;
  display: none;
}
</style>
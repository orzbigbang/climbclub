<script setup>
import { ref, useTemplateRef, onMounted, onBeforeUnmount } from 'vue';
import BIRDS from 'vanta/dist/vanta.birds.min'
import DOTS from 'vanta/dist/vanta.dots.min'

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
})

onBeforeUnmount(() => {
  if (vantaEffect) {
    vantaEffect.destroy()
  }
})

import LoginButton from './LoginButton.vue';
const sec = ref()
</script>

<template>
<div class="main-bg" ref='vantaRef'>
  <div class="button-wrapper pos-rel z-10 flex-between">
    <div class="github">
      <a class="logo-wrapper flex-between" href="https://github.com/orzbigbang/climbclub" target="_blank">
        <img class="logo" src="@/assets/githublogo.png" alt="GitHub Octocat Logo" />
        <span class="placeholder"></span>
        <span>Github</span>
      </a>
    </div>
    <LoginButton class="login-button" @mouse-hover="() => {sec = '5s'}" @mouse-leave="() => {sec = '20s'}"/>
  </div>

  <div class="text">
    <h1>Let's Climb!</h1>
    <p>Aim high and get higher</p>
  </div>
</div>
</template>

<style lang='less' scoped>
.main-bg {
  width: 100%;
  height: 80vh;
  z-index: 1;
  padding: 2rem;
  color: white;

  .github {
    padding: 10px;
    font-size: 16px;
    font-weight: 500;

    .logo-wrapper {
      .logo {
        width: 20px;
        height: 20px;
      }

      .placeholder {
        display: block;
        width: 5px;
      }
    }
  }

  .text {
    position: absolute;
    left: 10%;
    top: 55%;
    display: flex;    
    flex-direction: column;
    justify-content: space-around;
    align-items: start;

    h1 {
      font-size: 48px;
      font-weight: 700;
    }

    p {
      font-size: 20px;
      font-weight: 400;
    }
  }
}
</style>
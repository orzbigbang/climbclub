<script setup>
import { onMounted, onUnmounted } from 'vue';
import { ScrambleTextPlugin } from 'gsap-trial/dist/ScrambleTextPlugin'
import { getRandomNumber } from '@/compositions/randomThing'

gsap.registerPlugin(ScrambleTextPlugin)
let interval = null
let interval2 = null
const intervalMS = 6000
const interval2MS = 7000
const firstChild = 1
const secondChild = 2
const step = 6
const text = "Developing "
const chars = "0123456789abcdefXOABC"
const tl = gsap.timeline({defaults: {duration: 2, ease: "none"}});

const randomScrambleText = (nth) => {
  const randomNumber = getRandomNumber(0, step)
  const elements = document.querySelectorAll(`.ribbon:nth-child(${nth}) .block:nth-child(${step}n - ${randomNumber})`)
  tl.to(elements, {duration: 2, scrambleText:{text, chars}})
}

onMounted(() => {
  randomScrambleText(firstChild)
  randomScrambleText(secondChild)
  interval = setInterval(randomScrambleText, intervalMS, firstChild)
  interval2 = setInterval(randomScrambleText, interval2MS, secondChild)
})

onUnmounted(() => {
  if (interval) {
    clearInterval(interval)
  }
  if (interval2) {
    clearInterval(interval2)
  }
  tl.kill()
})
</script>

<template>
  <div class="container flex-col-center">
    <div class="ribbon-wrapper flex-col-between">
      <div class="ribbon flex-center" v-for="_ in 2">
        <div class="block" v-for="_ in 100">
          {{ text }}
        </div>
      </div>
    </div>
  </div>
</template>
    
<style lang='less' scoped>
@color: #333;

  .container {
    height: 100vh;
    overflow: hidden;  // TODO for develop only
    font-family: "Smooch Sans";
    color: @color;
    font-size: 48px;
    background-image: url("noise-bg.png");
    
    .ribbon-wrapper {
      width: 100vw;
      height: 40vh;

      .ribbon {
        height: 35%;
        border-bottom: 2px solid @color;
        border-top: 2px solid @color;
        gap: 1%;
        transform-origin: center;
        
        &:nth-child(1) {
          transform: rotateZ(-10deg) translateY(100px);
        }
        
        &:nth-child(2) {
          transform: rotateZ(15deg) translateY(-100px);
        }
        
        .block {
          width: 150px;
          animation: move 60s infinite linear;
        }
      }
    }
  }

  @keyframes move {
    50% {
      transform: translateX(-3000px);
    }
  }
</style>
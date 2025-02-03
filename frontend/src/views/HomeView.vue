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
  
<script setup>
import { onMounted } from 'vue';
import {ScrambleTextPlugin} from 'gsap-trial/dist/ScrambleTextPlugin'
const text = "Developing "
const chars = "0123456789abcdef"

onMounted(() => {
  const element = document.querySelectorAll(".block")
  const tl = gsap.timeline({defaults: {duration: 2, ease: "none"}});
  gsap.registerPlugin(ScrambleTextPlugin)
  // tl.to(element, {duration: 2, scrambleText:{text:text, chars:chars, revealDelay:0.5, tweenLength:false}})
})
</script>
  
<style lang='less' scoped>
@color: #333;

  .container {
    min-height: 100vh;
    
    .ribbon-wrapper {
      width: 100vw;
      height: 40vh;

      .ribbon {
        height: 35%;
        // width: 100vw;
        color: @color;
        font-size: 48px;
        font-weight: 400;
        font-family: "Smooch Sans";
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
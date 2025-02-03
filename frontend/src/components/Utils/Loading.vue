<script setup>
import { useShowStore } from '@/stores/show';
import { storeToRefs } from 'pinia';

const { loading } = storeToRefs(useShowStore())

const ballCount = 36
const containerSize = 150
const ballRadius = containerSize / 2
const rotate = 360 / ballCount
</script>

<template>
  <transition name="loading-fade">
    <div v-if="loading" class="loading pos-fix z-10000 flex-center">
      <div class="dot" v-for="i in ballCount" :key="i" :style="{ transform: `rotate(${i * rotate}deg) translateY(-${ballRadius}px)` }"></div>
    </div>
  </transition>
</template>

<style lang='less' scoped>
@ballCount: 36;
@ballSize: 10px;
@containerSize: 150px;
@animationDuration: 2s;

.loading {
  width: @containerSize;
  height: @containerSize;
  width: 100vw;
  height: 100vh;
  background-color: rgba(255, 255, 255, .8);

  .dot {
    position: absolute;
    left: 50%;
    top: 50%;
    width: @ballSize;
    height: @ballSize;
    margin-left: -@ballSize / 2;
    margin-top: -@ballSize / 2;
    background-color: transparent;
    border-radius: 50%;
    transform-origin: center;
    perspective: 70px;
    transform-style: preserve-3d;

    &::before,
    &::after {
      content: '';
      position: absolute;
      width: 100%;
      height: 100%;
      background-color: inherit;
      border-radius: inherit;
    }

    &::before {
      background-color: #000;
      top: -100%;
      animation: moveBlack @animationDuration infinite;
    }

    &::after {
      background-color: #aaa;
      top: 100%;
      animation: moveWhite @animationDuration infinite;
    }
  }
}

.loop(@i) when(@i <= @ballCount) {
  .dot:nth-child(@{i}) {
    &::before, 
    &::after {
      animation-delay: -(@animationDuration / @ballCount) * 6 * @i;
    }
  }
  .loop(@i + 1);
}
.loop(1);

@keyframes moveBlack {
  0% {
    animation-timing-function: ease-in;
  }
  25% {
    transform: translate3d(0, 100%, @ballSize);
    animation-timing-function: ease-out;
  }
  50% {
    transform: translate3d(0, 200%, 0);
    animation-timing-function: ease-in;
  }
  75% {
    transform: translate3d(0, 100%, -@ballSize);
    animation-timing-function: ease-out;
  }
}

@keyframes moveWhite {
  0% {
    animation-timing-function: ease-in;
  }
  25% {
    transform: translate3d(0, -100%, -@ballSize);
    animation-timing-function: ease-out;
  }
  50% {
    transform: translate3d(0, -200%, 0);
    animation-timing-function: ease-in;
  }
  75% {
    transform: translate3d(0, -100%, @ballSize);
    animation-timing-function: ease-out;
  }
}

.loading-fade-enter-active,
.loading-fade-leave-active {
  transition: all .3s ease;
}

.loading-fade-enter-from,
.loading-fade-leave-to {
  opacity: 0;
}
</style>
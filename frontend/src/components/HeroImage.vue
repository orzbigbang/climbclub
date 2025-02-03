<script setup>
import { useTemplateRef, onMounted, onBeforeUnmount } from 'vue';
import BIRDS from 'vanta/dist/vanta.birds.min'
import DOTS from 'vanta/dist/vanta.dots.min'
import GitHubBotton from './Buttons/GitHubBotton.vue';
import LoginButton from './Buttons/LoginButton.vue';
import { useShowStore } from '@/stores/show';

const showStore = useShowStore()
showStore.loading = true

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
  showStore.loading = false
})

onBeforeUnmount(() => {
  if (vantaEffect) {
    vantaEffect.destroy()
  }
})
</script>

<template>
<div class="main-bg" ref='vantaRef'>
  <slot>
    <div class="button-wrapper pos-rel z-10 flex-between">
      <GitHubBotton/>
      <LoginButton/>
    </div>
  </slot>

  <div class="text-wrapper pos-abs z-10 flex-col-between">
    <h1>Let'<span class="rotating rotating-3">s</span> H<span class="rotating rotating-1">i</span>k<span class="rotating rotating-2">i</span>ng!</h1>
    <p>Aim high and get higher</p>
  </div>
</div>
</template>

<style lang='less' scoped>
@base: 10px;

.main-bg {
  width: 100%;
  height: 80vh;
  padding: 3 * @base;
  color: white;

.text-wrapper {
  left: 10%;
  top: 55%;
  align-items: start;

  h1 {
    font-size: 4.8 * @base;
    font-weight: bold;

    .rotating {
      display: inline-block;
      perspective: 10 * @base;
      transform-style: preserve-3d;
    }
    
    .rotating-1 {
      color: pink;
      animation: x-rotating 8s ease-in-out infinite;
    }

    .rotating-2 {
      color: pink;
      animation: x-rotating 10s ease-in-out infinite reverse;
    }

    .rotating-3 {
      color: lightgreen;
      animation: x-rotating 6s ease-in-out infinite reverse;
    }
  }

    p {
      font-size: 2 * @base;
      font-weight: normal;
    }
  }
}

@keyframes x-rotating {
  30% {
    transform: rotate3d(1, 0, 0, 0deg) scale(1);
  }
  50% {
    transform: rotate3d(1, 0, 0, 1080deg) scale(1.2);
  }
  60% {
    transform: rotate3d(1, 0, 0, 720deg) scale(1.2);
  }
  100% {
    transform: rotate3d(1, 0, 0, 360deg) scale(1);
  }
}

.v-enter-active,
.v-leave-active {
  transition: opacity .2s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
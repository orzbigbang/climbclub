<script setup>

</script>

<template>
<div class="text-wrapper pos-abs z-10 flex-col-between">
  <h1>Let'<span class="rotating rotating-3">s</span> H<span class="rotating rotating-1">i</span>k<span class="rotating rotating-2">i</span>ng!</h1>
  <p>Aim high and get higher</p>
</div>
</template>

<style lang='less' scoped>
@base: 10px;

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
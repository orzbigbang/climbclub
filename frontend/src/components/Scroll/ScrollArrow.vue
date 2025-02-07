<script setup>

</script>

<template>
<div class="scroll-indicator flex-col-center pos-fix pos-x-center z-1000">
  <div class="mouse pos-rel">
    <div class="scroll-dot pos-abs pos-x-center"></div>
  </div>
  <p class="scroll-text">Scroll Down</p>
</div>

</template>

<style lang='less' scoped>
@color: rgba(0, 0, 0, 0.5);
@base: 8px;

.scroll-indicator {
  width: 10 * @base;
  gap: 0.5 * @base;
  background: transparent;
  bottom: 5%;
  
  .mouse {
    width: 3 * @base;
    height: 5 * @base;
    border: 2px solid @color;
    border-radius: 1.5 * @base;

    .scroll-dot {
      width: .8 * @base;
      height: .8 * @base;
      background-color: @color;
      border-radius: 50%;
      top: 0.8 * @base;
      animation: scroll-animation 1.5s infinite;
    }
  }

  .scroll-text {
    font-size: 1.4  * @base;
    color: @color;
    animation: fade-text 2s infinite;
  }
}


@keyframes scroll-animation {
  0% {
    top: 1 * @base;
    opacity: 1;
  }
  50% {
    top: 3 * @base;
    opacity: 0.5;
  }
  100% {
    top: 3.5 * @base;
    opacity: 0;
  }
}


@keyframes fade-text {
  0%, 100%{
    opacity: 0.3;
  }
  50% {
    opacity: 1;
  }
}

</style>
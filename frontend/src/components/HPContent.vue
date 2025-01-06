<script setup>
import { ref } from "vue";

const sec = ref("20s")
</script>

<template>
  <div class="bg-move flex-center pos-rel">
  </div>
</template>

<style lang='less' scoped>
.bg-move {
  min-height: 20vh;
  background: linear-gradient(155deg, pink, rgb(241, 167, 140), rgb(237, 147, 114), plum, rgb(251, 163, 213), plum, rgb(242, 141, 105), rgb(244, 165, 136), pink);
  background-size: 1000%;
  background-position-x: left;
  background-position-y: top;
  animation: bg-move v-bind(sec) linear infinite;
  z-index: 1;
}

@keyframes bg-move {
  0%, 100% {
    background-size: 1000%;
  }
  15%, 85% {
    background-size: 800%;
    background-position-x: 30%;
  }
  50% {
    background-size: 700%;
    background-position-x: right;
  }
}
</style>
<script setup>
import router from '@/router';
</script>

<template>
<a class="pos-rel" @mouseleave="$emit('mouse-leave')" @mouseover="$emit('mouse-hover')" @click="() => {router.push('/home')}">Login!</a>
</template>

<style lang='less' scoped>
a {
  display: inline-block;
  width: 8rem;
  height: 3rem;
  line-height: 3rem;
  text-align: center;
  background-color: skyblue;
  color: #fff;
  font-weight: bold;
  background: linear-gradient(90deg, #03a9f4, #f441a5, #ffeb3b, #03a9f4);
  background-size: 400%;
  border-radius: 10px;
  cursor: pointer;
  animation: Hikari 15s linear infinite;

  &:hover {
    animation: Hikari 2s linear infinite;

    &::before {
      filter: blur(20px);
      opacity: 1;
    }
  }

  &::before {
    content: '';
    position: absolute;
    left: -5px;
    top: -5px;
    right: -5px;
    bottom: -5px;
    z-index: -1;
    background: linear-gradient(90deg, #03a9f4, #f441a5, #ffeb3b, #03a9f4);
    background-size: 400%;
    border-radius: 10px;
    opacity: 0;
    transition: all .3s;
  }
}

@keyframes Hikari {
  0% {
    background-position: 0 0;
  }
  100% {
    background-position: 400% 0;
  }
}
</style>
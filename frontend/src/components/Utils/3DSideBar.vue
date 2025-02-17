<script setup>

  const props = defineProps({
    items: {
      type: Array,
      required: true
    }
  })
</script>

<template>
  <ul>
    <li v-for="item, index in props.items" :key="index" :style="`--i:${props.items.length - index};`" @click="item.func">{{ item.name }}</li>
  </ul>
</template>
  
<style scoped lang='less'>
ul {
  transform: skewY(-12deg);
  position: fixed;
  bottom: 5rem;
  left: 5rem;

  li {
    width: 10rem;
    height: 3rem;
    padding-left: .5rem;
    line-height: 3rem;
    color: #bbb;
    letter-spacing: 0.05rem;
    background-color: rgb(35, 29, 35);
    border-bottom: 1px solid #444;
    position: relative;
    transition: .3s;
    z-index: var(--i);

    &::after, &::before {
      content: "";
      display: block;
      position: absolute;
      transition: .3s;
    }

    &::before {
      width: 2.5rem;
      height: 3rem;
      background-color: rgb(17, 15, 17);
      left: -2.5rem;
      transform: skewY(36deg);
      transform-origin: right top;
    }

    &::after {
      width: 10rem;
      height: 1.8rem;
      background-color: rgb(42, 35, 42);
      top: -1.8rem;
      left: 0;
      transform: skewX(54deg);
      transform-origin: bottom;
    }

    &:hover {
      color: #fff;
      cursor: pointer;
      background-color: rgb(46, 106, 234);
      transform: translateX(50%);

      &::before {
        background-color: rgb(31, 57, 113);
      }

      &::after {
        background-color: rgb(81, 134, 249);
      }
    }
  }
}
  
</style>
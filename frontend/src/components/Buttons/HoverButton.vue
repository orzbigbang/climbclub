<script setup>
import IconThumb from '@/components/icons/IconThumb.vue';
</script>

<template>
  <a class="hover-button flex-center" >
    <IconThumb :size="45"/>
  </a>
</template>
  
<style lang='less' scoped>
@property --fill {
  syntax: "<percentage>";
  inherits: true;
  initial-value: 0%;
}

  .hover-button {
    inline-size: 2.5rem;
    color: #636363;
    background-color: #2b2b2b;
    border-radius: 50%;
    transition: color 0.5s 0.3s ease-out;
    cursor: pointer;
    position: relative;

    &::before,
    &::after {
      content: '';
      position: absolute;
      inset: -5px;
      border-radius: inherit;
      background: conic-gradient(greenyellow var(--fill), transparent var(--fill));
      z-index: -1;
      transition: --fill 0.3s ease-in-out;
      pointer-events: none;
    }

    &:hover,
    &:focus-visible,
    &:focus-within {
      color: greenyellow;
      outline: 1px solid transparent;
      --fill: 100%;
    }
  }
</style>
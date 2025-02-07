<script setup>
import GithubIcon from '@/components/icons/IconGithub.vue';
import PopupIcon from '@/components/icons/IconPopup.vue';

</script>

<template>
  <div class="github">
    <a class="logo-wrapper flex-between" href="https://github.com/orzbigbang/climbclub" target="_blank">
      <GithubIcon/>
      <span>Github</span>
      <PopupIcon class="popup"/>
    </a>
  </div>
</template>

<style lang='less' scoped>
@base: 10px;

.github {
  padding: 1 * @base;
  font-size: 1.6 * @base;
  font-weight: normal;
  background-clip: text;

  .logo-wrapper {
    gap: 0.5 * @base;

    .popup {
      margin-left: -3px;
      opacity: 0;
      transition: all .15s linear;
    }

    &:hover {
      .popup {
        opacity: 1;
        transform: rotateZ(15deg);
      }
    }
  }
}
</style>

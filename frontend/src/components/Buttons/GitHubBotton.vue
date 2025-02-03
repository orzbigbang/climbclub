<script setup>

</script>

<template>
  <div class="github">
    <a class="logo-wrapper flex-between" href="https://github.com/orzbigbang/climbclub" target="_blank">
      <img class="logo" src="@/assets/githublogo.png" alt="GitHub Octocat Logo" />
      <span>Github</span>
    </a>
  </div>
</template>

<style lang='less' scoped>
@base: 10px;

.github {
  padding: 1 * @base;
  font-size: 1.6 * @base;
  font-weight: normal;

  .logo-wrapper {
    gap: 0.5 * @base;

    .logo {
      width: 2 * @base;
      height: 2 * @base;
    }
  }
}
</style>
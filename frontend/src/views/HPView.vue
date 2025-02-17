<script setup>
import { ref, onMounted, watch } from 'vue';

import HeroImage from '@/components/HeroImage.vue';
import ScrollContent from '@/components/Scroll/ScrollContent.vue';
import ScrollArrow from '@/components/Scroll/ScrollArrow.vue';
import Slogan from '@/components/Slogan.vue';
import GitHubBotton from '@/components/Buttons/GitHubBotton.vue';
import LoginButton from '@/components/Buttons/LoginButton.vue';

import { useShowStore } from '@/stores/show';
const showStore = useShowStore();

const heroLoaded = ref(false);
const scrollContentLoaded = ref(false);

// 创建加载处理函数
const handleLoading = () => {
  const loadingPromise = Promise.all([
    // 第一次加载时至少等待2秒
    new Promise(resolve => {
      const isFirstVisit = !sessionStorage.getItem('hasVisited');
      const delay = isFirstVisit ? 2000 : 0;
      setTimeout(() => {
        if(isFirstVisit) sessionStorage.setItem('hasVisited', 'true');
        resolve();
      }, delay);
    }),
    new Promise(resolve => {
      if (heroLoaded.value) resolve();
      else watch(heroLoaded, (val) => val && resolve());
    }),
    new Promise(resolve => {
      if (scrollContentLoaded.value) resolve();
      else watch(scrollContentLoaded, (val) => val && resolve());
    })
  ]);

  showStore.showLoading(loadingPromise);
};

onMounted(() => {
  handleLoading();
});
</script>

<template>
  <HeroImage @loaded="heroLoaded = true">
    <div class="button-wrapper pos-rel z-10 flex-between">
      <GitHubBotton />
      <LoginButton />
    </div>
    <Slogan />
  </HeroImage>

  <ScrollContent @loaded="scrollContentLoaded = true" />
  <ScrollArrow />
</template>

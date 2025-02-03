<script setup>
import AITalk from '@/components/Utils/AITalk.vue';
import HoverButton from '@/components/Buttons/HoverButton.vue';
import GlobalNotification from '@/components/Utils/GlobalNotification.vue'
import Loading from '@/components/Utils/Loading.vue';
import { onMounted, watch } from 'vue';
import { useAccountStore } from '@/stores/account';
import { useNavigationStore } from '@/stores/navigation';
import { storeToRefs } from 'pinia'
import router from '@/router';

const accountStore = useAccountStore();
const navigationStore = useNavigationStore();
const { navigationTarget } = storeToRefs(navigationStore);

// 监听导航状态变化
watch(navigationTarget, (newTarget) => {
  if (newTarget.path) {
    router.push({
      path: newTarget.path,
      query: newTarget.query
    });
  }
}, { deep: true });

onMounted(async () => {
  await accountStore.initializeAuth();
})
</script>

<template>
  <!-- <AITalk/> -->
  <!-- <HoverButton/> -->
  <Loading />
  <GlobalNotification />
  <RouterView></RouterView>
</template>123

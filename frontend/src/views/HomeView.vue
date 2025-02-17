<script setup>
import SideBar from '@/components/SideBar.vue';
import Navigation from '@/components/Navigation.vue';

import { useNavigationStore } from '@/stores/navigation';
const navigationStore = useNavigationStore(); 

const items = [
  {
    name: 'RECOLLECTION',
    icon: '',
    func: () => {}
  },
  {
    name: 'EXPLORE',
    icon: '',
    func: () => {}
  },
  {
    name: 'MAILBOX',
    icon: '',
    func: () => {}
  },
  {
    name: 'SHOP',
    icon: '',
    func: () => {}
  },
  {
    name: 'NEWS',
    icon: '',
    func: () => {}
  },
  {
    name: 'SUPPORT',
    icon: '',
    func: () => {}
  },
]
</script>

<template>
  <div class="bg"></div>
  <SideBar :items="items"/>
</template>

<style lang='less' scoped>
.bg {
  width: 100vw;
  height: 100vh;
  background-color: @homeBackgroundColor;
}


</style>
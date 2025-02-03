<script setup>
import { storeToRefs } from 'pinia';
import {useAccountStore} from '@/stores/account';
import { useNavigationStore } from '@/stores/navigation';
import Cookies from 'js-cookie';
import UserIcon from '@/components/icons/IconUser.vue';
import IconSupport from '@/components/icons/IconSupport.vue';
import LogoutIcon from '@/components/icons/IconLogout.vue';
import endpoints from '@/api/endpoints';
import { ref } from 'vue';

const accountStore = useAccountStore();
const navigationStore = useNavigationStore();
const { isLoggedIn } = storeToRefs(accountStore);
const showFullList = ref(false);

const profileList = [
  {
    name: 'Home',
    icon: UserIcon,
    action: () => {
      navigationStore.navigateHome();
    }
  },  
  {
    name: 'Support',
    icon: IconSupport, 
    action: () => {
      navigationStore.navigateSupport();
    }
  },
  {
    name: 'Logout',
    icon: LogoutIcon,
    action: () => {
      accountStore.logout();
      navigationStore.navigateMain();
    }
  }
]
</script>

<template>
  <a class="login-button-wrapper pos-rel" 
    v-if="!isLoggedIn" 
    @mouseleave="$emit('mouse-leave')" 
    @mouseover="$emit('mouse-hover')" 
    @click="() => {navigationStore.navigateLogin(endpoints.home)}">
    Login!
  </a>
  <div v-else class="profile-wrapper" @mouseleave="showFullList = false" @mouseover="showFullList = true">
    <div class="profile-item" @click="profileList[0].action">
      <span class="item-name pos-rel">
        <component :is="profileList[0].icon" class="icon-before" />
        {{ profileList[0].name }}
      </span>
    </div>
    <Transition>
      <div v-show="showFullList" class="profile-list flex-col-between">
        <div class="profile-item" v-for="item in profileList.slice(1)" :key="item.name" @click="item.action">
          <span class="item-name pos-rel">
            <component :is="item.icon" class="icon-before" />
            {{ item.name }}
          </span>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style lang='less' scoped>
@base: 14px;

.login-button-wrapper {
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

.profile-wrapper {
  width: 8rem;
  height: auto;
  min-height: 3rem;
  line-height: 3rem;
  text-align: center;
  text-decoration: none;
  transition: all .5s;
  position: relative;

  .profile-list {
    position: absolute;
    width: 100%;
  }

  .profile-item {
    opacity: 0.5;
    cursor: pointer;
    transition: all .2s ease-in-out;

    &:hover {
      opacity: 1;
      transform: scale(1.2);
    }

    @color: #fff;
    .item-name {
      color: @color;
      padding-left: 30px;
      position: relative;

      .icon-before {
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 20px;
        height: 20px;
        color: @color;
      }
    }
  }
}
</style>
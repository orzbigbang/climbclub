<script setup>
import IconGoogle from '@/components/icons/IconGoogle.vue';
import IconDiscord from '@/components/icons/IconDiscord.vue';
import ForestHouse from '@/components/ForestHouse.vue';
import { useAccountStore } from '@/stores/account';
import { useNavigationStore } from '@/stores/navigation';
import { useShowStore } from '@/stores/show';

const accountStore = useAccountStore()
const navigationStore = useNavigationStore()
const showStore = useShowStore()

const loginSuccess = (response) => {
  accountStore.login(response)
  showStore.showLoading(
    new Promise((resolve) => {setTimeout(resolve, 1000);}), 
    navigationStore.navigateHome()
  )
}

const signupSuccess = (response) => {
  loginSuccess(response)
}

// 添加SSO登录方法
// 统一的OAuth弹窗处理函数
const openOAuthPopup = (url, title) => {
  const width = 500;
  const height = 600;
  const left = window.screenX + (window.outerWidth - width) / 2;
  const top = window.screenY + (window.outerHeight - height) / 2;

  const popup = window.open(
    url,
    title,
    `width=${width},height=${height},left=${left},top=${top}`
  );

  return new Promise((resolve) => {
    window.addEventListener('message', (event) => {
      console.log(`output-event`,event)
      if (event.origin === window.location.origin) {
        if (event.data.type === 'oauth-callback') {
          popup.close();
          resolve(event.data.code);
        }
      }
    }, false);
  });
};

const loginWithGoogle = async () => {
  const clientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;
  const redirectUri = `${window.location.origin}/oauth/callback/google`;
  
  const params = new URLSearchParams({
    client_id: clientId,
    redirect_uri: redirectUri,
    response_type: 'code',
    scope: 'email profile',
    access_type: 'offline',
    prompt: 'consent'
  });

  const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?${params.toString()}`;
  const code = await openOAuthPopup(authUrl, 'Google登录');
  
  // TODO: 处理授权码
  console.log(code);
};

const loginWithDiscord = async () => {
  const clientId = import.meta.env.VITE_DISCORD_CLIENT_ID;  
  const redirectUri = `${window.location.origin}/profile`;
  const params = new URLSearchParams({
    client_id: clientId,
    redirect_uri: redirectUri,
    response_type: 'code',
    scope: 'identify email',
  });
  
  const authUrl = `https://discord.com/oauth2/authorize?${params.toString()}`;
  const code = await openOAuthPopup(authUrl, 'Discord登录');
  // TODO: 处理授权码
  console.log(code);
};
</script>

<template>
  <div class="wrapper">
    <div class="bg">
      <ForestHouse /> 
    </div>
    <div class="divider"></div>
    <div class="right-section">
      <router-view v-slot="{ Component }">
        <transition name="route-change" mode="out-in">
          <component :is="Component" @login-success="loginSuccess" @signup-success="signupSuccess"/>
        </transition>
      </router-view>
      <div class="sso-provider-wrapper">
        <button class="sso-button google" @click="loginWithGoogle">
          <IconGoogle size="24"/>
          使用 Google 账号登录
        </button>
        <button class="sso-button discord" @click="loginWithDiscord">
          <IconDiscord size="24"/>
          使用 Discord 账号登录
        </button>
      </div>
    </div>
  </div>
</template>
  
<style lang='less' scoped>
.wrapper {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  height: 100vh;
  margin: 0 auto;
  background-color: #fff;

  // 左侧背景区域
  .bg {
    width: 65%;
    height: 100%;
    position: relative;
    overflow: hidden;
  }

  // 分隔线
  .divider {
    width: 0.5px;
    height: 60%;
    background-color: #ccc;
  }

  // 右侧内容区域
  .right-section {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;

    // 表单容器样式
    :deep(.oauth-container) {
      width: 100%;
      margin: 0 auto;
      
      .form-wrapper {
        width: 75%;
        margin: 0 auto;
        padding: 30px;
        border: 1px solid #ccc;
        border-radius: 5px;
        background-color: #f9f9f9;

        .form-title {
          text-align: center;
          margin-bottom: 30px;
        }

        // 表单元素样式
        .input-item {
          margin: 8px 0;
        }

        .error-message {
          color: red;
          margin-top: 10px;
          font-size: 14px;
        }

        // 按钮样式
        .login-button, 
        .next-button {
          background-color: #4285f4;
          color: white;
          
          &:hover {
            background-color: #357abd;
          }
        }

        .register-button {
          background-color: transparent;
          color: #007bff;
          border: 1px solid #007bff;

          &:hover {
            background-color: #daeaf8;
          }
        }
      }

      // 输入框和按钮的基础样式
      label {
        display: block;
        margin-bottom: 5px;
      }

      input {
        width: 100%;
        height: 40px;
        padding: 8px;
        border: 1px solid #ddd;
        border-radius: 4px;
        transition: all .2s ease-in-out;

        &:hover {
          border-color: #9ab9ec;
        }
        
        &:focus {
          outline: none;
          border-color: #4285f4;
        }
      }

      button {
        width: 100%;
        padding: 10px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 14px;
      }
    }

    // SSO登录区域样式
    .sso-provider-wrapper {
      width: 75%;
      margin: 20px auto 0;
      display: flex;
      flex-direction: column;
      gap: 12px;
      
      .sso-button {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 12px 20px;
        border: none;
        border-radius: 4px;
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: background-color 0.3s ease;
        color: white;
      
        &.google {
          background-color: #4285f4;
      
          &:hover {
            background-color: #357abd;
          }
        }
      
        &.discord {
          background-color: #5865f2;
      
          &:hover {
            background-color: #4752c4;
          }
        }
      }
    }
  }
}

// 路由切换动画
.route-change-enter-active,
.route-change-leave-active {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.route-change-enter-from {
  opacity: 0;
  transform: translate3d(50px, 0, 0) scale(0.95) rotate(2deg);
}

.route-change-leave-to {
  opacity: 0;
  transform: translate3d(-50px, 0, 0) scale(0.95) rotate(-2deg);
}
</style>
<script setup>
import { ref, watch } from 'vue';
import { login } from '@/api/login';
import userService from '@/api/userService';
import IconSuccess from '@/components/icons/IconSuccess.vue';
import IconEye from '@/components/icons/IconEye.vue';
import { useNavigationStore } from '@/stores/navigation';

const navigationStore = useNavigationStore();
const emit = defineEmits(['login-success']);

const username = ref('');
const error = ref('')
const password = ref('');
const usernameValidated = ref(false);
const shake = ref(false);
const checkUserLoading = ref(false);
const checkUserSuccess = ref(false);
const showPassword = ref(false);
const loginLoading = ref(false);
const loginSuccess = ref(false);

// 添加延迟函数
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// 修改验证用户名函数
const validateUsername = async () => {
  if (username.value === '') {
    error.value = '用户名不能为空';
    shake.value = true;
    setTimeout(() => shake.value = false, 500);
    return;
  }

  if (!/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/.test(username.value)) {
    error.value = '用户名为邮箱';   
    shake.value = true;
    setTimeout(() => shake.value = false, 500);
    return;
  }

  checkUserLoading.value = true;
  error.value = '';
  
  try {
    // 创建并行的 Promise
    const [response] = await Promise.all([
      userService.hasUser(username.value),
      delay(500) // 确保至少 0.5 秒的加载时间
    ]);

    checkUserLoading.value = false;
    checkUserSuccess.value = true;
    // 延迟显示密码输入框，给足够时间显示成功动画
    setTimeout(() => {
      checkUserSuccess.value = false;
      usernameValidated.value = true;
    }, 800);
  } catch (err) {
    checkUserLoading.value = false;
    error.value = '用户名不存在';
    shake.value = true;
    setTimeout(() => shake.value = false, 500);
  }
}

// 如果正在输入的话，清空错误信息
watch(username, (newVal, oldVal) => {
  if (newVal !== '' || (newVal === '' && oldVal !== '')) {
    error.value = '';
  }
})

// 如果正在输入的话，清空错误信息
watch(password, (newVal, oldVal) => {
  if (newVal !== '' || (newVal === '' && oldVal !== '')) {
    error.value = '';
  }
})

// 修改登录处理函数
const loginHandler = async () => {
  loginLoading.value = true;
  let response = null;

  // 创建并行的 Promise, 确保至少 0.5 秒的加载时间
  await Promise.all([
    login(username.value, password.value).then((res) => {
      response = res;
      error.value = '';
    }).catch(() => {
      error.value = '密码错误';
      shake.value = true;
      setTimeout(() => shake.value = false, 500);
    }),
    delay(500)
  ]);

  loginLoading.value = false;

  if (response) {
    emit('login-success', response);
  }
}

// 跳转到注册页面
const goRegister = () => {
  navigationStore.navigateSignup();
}

// 切换到其他账户
const switchAccount = () => {
  usernameValidated.value = false;
  username.value = '';
  password.value = '';
  error.value = '';
}

const togglePassword = (show) => {
  showPassword.value = show;
};
</script>

<template>
<div class="oauth-container flex-col-between">
  <div class="form-wrapper">
    <h2 class="form-title">登录</h2>
    <form>
      <transition name="slide" mode="out-in">
        <div v-if="usernameValidated" key="password" class="input-group" :class="{ 'shake': shake }">
          <div class="password-wrapper">
            <div class="input-item password-input-wrapper">
              <input 
                :type="showPassword ? 'text' : 'password'" 
                id="password" 
                v-model="password" 
                placeholder="请输入密码" 
                required 
                autofocus
              />
              <div 
                class="eye-button"
                type="button"
                @mousedown.prevent="togglePassword(true)"
                @mouseup.prevent="togglePassword(false)"
                @mouseleave.prevent="togglePassword(false)"
              >
                <IconEye :class="{ 'active': showPassword }" />
            </div>
            </div>
          </div>
        </div>
        <div v-else key="username" class="input-item input-group" :class="{ 'shake': shake }">
          <input type="text" id="username" v-model="username" placeholder="请输入用户名/邮箱" required autofocus/>
        </div>
      </transition>
      <p v-if="error" class="error-message">{{ error }}</p>
      
      <button v-if="usernameValidated" class="input-item login-button" type="submit" @click.prevent="loginHandler">
        <template v-if="loginLoading">
          <div class="loading"></div>
        </template>
        <template v-else-if="loginSuccess">
          <div class="success">
            <IconSuccess />
          </div>
        </template>
        <template v-else>
          <span>登录</span>
        </template>
      </button>
      <button v-else class="input-item next-button" @click.prevent="validateUsername" :disabled="checkUserLoading || checkUserSuccess">
        <template v-if="checkUserLoading">
          <div class="loading"></div>
        </template>
        <template v-else-if="checkUserSuccess">
          <div class="success">
            <IconSuccess />
          </div>
        </template>
        <template v-else>
          <span>下一步</span>
        </template>
      </button>
    </form>

    <div class="register-wrapper">
      <button class="input-item register-button" @click="goRegister">注册</button>
    </div>

    <transition name="fade">
      <div v-if="usernameValidated" class="function-wrapper">
        <a class="function-link" @click.prevent="switchAccount">
          <span>登录其他账户</span>
        </a>
        <div class="divider"></div>
        <a class="function-link" href="/oauth/reset-password">
          <span>忘记密码</span>
        </a>
      </div>
    </transition>
  </div>
</div>
</template>


<style lang='less' scoped>
// 优化滑动动画，添加挤压效果
.slide-enter-active,
.slide-leave-active {
  transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  transform-origin: center;
  position: relative;
}

.slide-enter-from {
  opacity: 0;
  transform: translate3d(50px, 0, 0) scaleX(0.8) scaleY(1.2);
}

.slide-leave-to {
  opacity: 0;
  transform: translate3d(-50px, 0, 0) scaleX(1.2) scaleY(0.8);
}

// 优化淡入淡出动画
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  transform-origin: center;
}

.fade-enter-from {
  opacity: 0;
  transform: translate3d(50px, 0, 0) scaleX(0.8) scaleY(1.2);
}

.fade-leave-to {
  opacity: 0;
  transform: translate3d(-50px, 0, 0) scaleX(1.2) scaleY(0.8);
}

// 加载动画
.loading {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 2px solid #ffffff;
  border-radius: 50%;
  border-top-color: transparent;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

// 成功动画
.success {
  display: inline-block;
  font-size: 20px;
  animation: success-in 0.3s ease-out;
}

@keyframes success-in {
  from {
    transform: scale(0);
  }
  to {
    transform: scale(1);
  }
}

// 密码输入框样式
.password-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.password-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;

  input {
    padding-right: 40px;
  }

  .eye-button {
    position: absolute;
    right: 8px;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    padding: 4px;
    cursor: pointer;
    color: #999;
    opacity: 0.5;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;

    &:hover {
      opacity: 1;
    }

    .active {
      color: #4285f4;
    }
  }
}

// 按钮样式
.next-button {
  position: relative;
  height: 40px;
  transition: all 0.3s ease;
  
  &:disabled {
    cursor: not-allowed;
    opacity: 0.9;
    transform: scale(0.98);
  }

  span {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
  }
}

// 抖动动画
@keyframes shake {
  0%, 100% {
    transform: translateX(0);
  }
  20%, 60% {
    transform: translateX(-4px);
  }
  40%, 80% {
    transform: translateX(4px);
  }
}

.shake {
  animation: shake 0.4s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
}

// 错误信息样式
.error-message {
  color: #ff4d4f;
  font-size: 14px;
  margin-top: -8px;
  margin-bottom: 8px;
}

.function-wrapper {
  margin-top: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  font-size: 14px;

  .function-link {
    color: #666;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.3s ease;
    
    &:hover {
      color: #000;
    }

    span {
      position: relative;
      
      &::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 100%;
        height: 1px;
        background-color: #666;
        transform: scaleX(0);
        transition: transform 0.2s ease;
        transform-origin: center;
      }
    }

    &:hover span::after {
      transform: scaleX(1);
    }
  }

  .divider {
    width: 1px;
    height: 14px;
    background-color: #ddd;
  }
}

// 优化淡入淡出动画
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
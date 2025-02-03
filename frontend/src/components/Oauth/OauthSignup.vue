<script setup>
import { ref, watch } from 'vue';
import { register } from '@/api/login';
import userService from '@/api/userService';
import IconSuccess from '@/components/icons/IconSuccess.vue';
import IconEye from '@/components/icons/IconEye.vue';
import { useNavigationStore } from '@/stores/navigation';
import { useShowStore } from '@/stores/show'

const showStore = useShowStore()
const navigationStore = useNavigationStore();
const emit = defineEmits(['signup-success']);

const username = ref('');
const password = ref('');
const error = ref('');
const usernameValidated = ref(false);
const shake = ref(false);
const loading = ref(false);
const success = ref(false);
const showPassword = ref(false);
const confirmPassword = ref('');
const passwordShake = ref(false);
const confirmPasswordShake = ref(false);
const registerLoading = ref(false);
const registerSuccess = ref(false);

// 添加延迟函数
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// 验证用户名函数
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

  loading.value = true;
  error.value = '';

  // 创建并行的 Promise, 确保至少 0.5 秒的加载时间
  let hasUser = false;
  await Promise.all([
    userService.hasUser(username.value).then(() => {
      hasUser = true;
    }).catch(() => {
      hasUser = false;
    }),
    delay(500)
    ]
  );
  
  // 如果用户存在，显示错误
  if (hasUser) {
    loading.value = false;
    shake.value = true;
    error.value = '用户名已存在';
    setTimeout(() => shake.value = false, 500);
  } else {
    loading.value = false;
    success.value = true;
    setTimeout(() => {
      success.value = false;
      usernameValidated.value = true;
    }, 800);
  }
}

// 密码的验证状态
const passwordValidation = ref({
  length: false,
  hasLetter: false,
  hasNumber: false,
  isValid: false,
  isMatching: false,
  isFocused: false
});

// 密码验证函数
const validatePassword = (pass) => {
  passwordValidation.value.length = pass.length >= 8;
  passwordValidation.value.hasLetter = /[a-zA-Z]/.test(pass);
  passwordValidation.value.hasNumber = /[0-9]/.test(pass);
  passwordValidation.value.isValid = 
    passwordValidation.value.length && 
    passwordValidation.value.hasLetter && 
    passwordValidation.value.hasNumber
};

// 监听密码的变化
watch(password, (newValue) => {
  // 验证密码
  validatePassword(newValue);

  // 如果密码验证通过，则验证确认密码
  if (passwordValidation.value.isValid) {
    passwordValidation.value.isMatching = newValue === confirmPassword.value;
  } else {
    passwordValidation.value.isMatching = false;
  }
});

// 监视修改确认密码
watch(confirmPassword, (newValue) => {
  // 如果密码验证通过，则验证确认密码
  if (passwordValidation.value.isValid) {
    passwordValidation.value.isMatching = newValue === password.value;
  } else {
    passwordValidation.value.isMatching = false;
  }
});

// 注册函数
const registerHandler = async () => {
  if (passwordValidation.value.isValid && passwordValidation.value.isMatching) {
    registerLoading.value = true;
    error.value = '';
    
    try {
      // 创建并行的 Promise, 确保至少 0.5 秒的加载时间
      let response = null;
      await Promise.all([
          register(username.value, password.value).then((res) => {
            response = res;
            registerSuccess.value = true
          }).catch(() => {
            registerSuccess.value = false
          }),
        delay(500)
      ]);
      
      if (registerSuccess.value) {
        handleSignupSuccess(response)
      } else {
        handleSignupError()
      }

    } finally {
      registerLoading.value = false;
      registerSuccess.value = false;
    }
  } else {
    error.value = '未通过密码验证';
    if (!passwordValidation.value.isValid) {
      passwordShake.value = true;
      setTimeout(() => passwordShake.value = false, 500);
    }
    if (!passwordValidation.value.isMatching) {
      confirmPasswordShake.value = true;
      setTimeout(() => confirmPasswordShake.value = false, 500);
    }
  }
}

// 显示注册成功通知
const handleSignupSuccess = (response) => {
  showStore.showNotification('注册成功！', 'success', 3000, () => {
    emit('signup-success', response)
  })
}

// 显示注册错误通知
const handleSignupError = () => {
  showStore.showNotification('注册失败！', 'error', 3000, () => {
    navigationStore.navigateSignup()
  })
}

// 如果正在输入的话，清空错误信息
watch(username, (newVal, oldVal) => {
  if (newVal !== '' || (newVal === '' && oldVal !== '')) {
    error.value = '';
  }
})

watch(password, (newVal, oldVal) => {
  if (newVal !== '' || (newVal === '' && oldVal !== '')) {
    error.value = '';
  }
})

const togglePassword = (show) => {
  showPassword.value = show;
};

const goLogin = () => {
  navigationStore.navigateLogin();
}

// 切换到其他账户
const switchAccount = () => {
  usernameValidated.value = false;
  username.value = '';
  password.value = '';
  confirmPassword.value = '';
  error.value = '';
}
</script>

<template>
  <div class="oauth-container flex-col-between">
    <div class="form-wrapper">
      <h2 class="form-title">注册</h2>
      <form>
        <transition name="slide" mode="out-in">
          <div v-if="usernameValidated" key="password" class="input-group" :class="{ 'shake': shake }">
            <div class="password-wrapper">
              <div class="input-item password-input-wrapper" :class="{ 'shake': passwordShake }">
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
            <div class="password-requirements">
              <p class="pw-indicator" :class="{ valid: passwordValidation.length }">- 密码长度至少8位</p>
              <p class="pw-indicator" :class="{ valid: passwordValidation.hasLetter }">- 包含英文字母</p>
              <p class="pw-indicator" :class="{ valid: passwordValidation.hasNumber }">- 包含数字</p>
            </div>
            <div class="confirm-password-wrapper">
              <div class="input-item password-input-wrapper" :class="{ 'shake': confirmPasswordShake }">
                <input 
                  type="password" 
                  id="confirmPassword" 
                  v-model="confirmPassword" 
                  placeholder="请确认密码" 
                  required 
                  @focus="passwordValidation.isFocused = true"
                />
              </div>
            </div>
            <div v-if="passwordValidation.isFocused && passwordValidation.isValid" class="password-requirements">
              <p class="pw-indicator" :class="{ valid: passwordValidation.isMatching }">
                - 两次输入的密码一致
              </p>
            </div>
          </div>
          <div v-else key="username" class="input-item input-group" :class="{ 'shake': shake }">
            <input type="text" id="username" v-model="username" placeholder="请输入用户名/邮箱" required autofocus/>
          </div>
        </transition>
        <p v-if="error" class="error-message">{{ error }}</p>
        
        <button 
          v-if="usernameValidated" 
          class="input-item login-button" 
          type="submit" 
          @click.prevent="registerHandler"
          :disabled="registerLoading || registerSuccess"
        >
          <template v-if="registerLoading">
            <div class="loading"></div>
          </template>
          <template v-else-if="registerSuccess">
            <div class="success">
              <IconSuccess />
            </div>
          </template>
          <template v-else>
            <span>注册</span>
          </template>
        </button>
        <button v-else class="input-item next-button" @click.prevent="validateUsername" :disabled="loading || success">
          <template v-if="loading">
            <div class="loading"></div>
          </template>
          <template v-else-if="success">
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
        <button class="input-item register-button" @click="goLogin">已有账户？登录</button>
      </div>

      <transition name="fade">
      <div v-if="usernameValidated" class="function-wrapper">
        <a class="function-link" @click.prevent="switchAccount">
          <span>返回输入用户名</span>
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

// 添加密码要求提示样式
.password-requirements {
  margin-top: 8px;
  font-size: 14px;
  color: #666;

  .pw-indicator {
    margin: 4px 0;
    transition: color 0.3s ease;
    
    &.valid {
      color: #4caf50;
    }
  }
}

.confirm-password-wrapper {
  margin-top: 16px;
}

// 确保抖动动画样式应用到密码输入框
.password-input-wrapper.shake {
  animation: shake 0.4s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
}

// 修改注册按钮样式
.login-button {
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

  .loading {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 2px solid #ffffff;
    border-radius: 50%;
    border-top-color: transparent;
    animation: spin 0.8s linear infinite;
  }

  .success {
    display: inline-block;
    font-size: 20px;
    animation: success-in 0.3s ease-out;
  }
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
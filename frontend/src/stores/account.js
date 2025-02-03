// 全局状态store
import { defineStore } from 'pinia';
import { ref } from 'vue';
import { validateTokenAndGetNewAccessToken } from '@/api/login';
import Cookies from 'js-cookie';
import { jwtDecode } from 'jwt-decode';

export const useAccountStore = defineStore('account', () => {
  const username = ref('')
  const aut = ref(99)
  const access_token = ref('')
  const isLoggedIn = ref(false)
  
  // 添加初始化方法
  const initializeAuth = async () => {
    // 通过refresh_token判断
    if (Cookies.get('refresh_token')) {
      try {
        const response = await validateTokenAndGetNewAccessToken();
  
        // 将新的access_token设置到accountStore
        access_token.value = response.access_token;

        // decode token 获取username
        const decodedToken = jwtDecode(response.access_token);
        username.value = decodedToken.username;
        aut.value = decodedToken.aut;

        isLoggedIn.value = true;
      } catch (error) {
        // 如果验证失败，清除无效的refresh_token
        Cookies.remove('refresh_token');
        isLoggedIn.value = false;
      }
    } else {
      isLoggedIn.value = false;
    }
  }

  const login = (response) => {
    const access_token_data = jwtDecode(response.access_token);
    access_token.value = response.access_token
    username.value = access_token_data.username
    aut.value = access_token_data.aut
    isLoggedIn.value = true
  }

  const logout = () => {
    Cookies.remove('refresh_token');
    isLoggedIn.value = false;
  }

  return { username, aut, access_token, isLoggedIn, initializeAuth, login, logout }
})

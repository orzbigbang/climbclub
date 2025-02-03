import axios from 'axios';
import { useAccountStore } from '@/stores/account'

let accountStore = null

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8080/api/v1',
  timeout: 5000
});

// 响应拦截器
axiosInstance.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    // 对响应错误做些什么
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // token过期或无效,清除token并跳转到登录页
          if (!accountStore) {
            accountStore = useAccountStore()
          }
          accountStore.clearToken();
          router.push('/oauth/login');
          break;
        case 403:
          // 权限不足
          console.error('没有权限访问该资源');
          break;
        case 404:
          // 请求的资源不存在
          console.error('请求的资源不存在');
          break;
        case 500:
          // 服务器错误
          console.error('服务器错误');
          break;
        default:
          console.error('发生错误:', error.message);
      }
    }
    return Promise.reject(error);
  }
);

// 请求拦截器
axiosInstance.interceptors.request.use(
  config => {
    if (!accountStore) {
      accountStore = useAccountStore()
    }
    // 从store中获取token
    if (accountStore.access_token) {
      config.headers['Authorization'] = `Bearer ${accountStore.access_token}`;
    }
    // 设置cookie
    config.withCredentials = true;
    return config;
  },
  error => {
    // 对请求错误做些什么
    console.log(`output->`,123)
    return Promise.reject(error);
  }
);

export default axiosInstance;

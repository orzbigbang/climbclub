import axiosInstance from '@/api/axiosInstance';
import JSEncrypt from 'jsencrypt';
import { Buffer } from 'buffer';

const endpoints = {
  publickey: '/account/publickey',
  login: '/account/login',
  signup: '/account/signup'
};

// 获取公钥
export const getPublicKey = async () => {
  const response = await axiosInstance.get(endpoints.publickey);
  return response.data;
};

// 用公钥加密密码
export const encryptPassword = async (password) => {
  const publicKey = await getPublicKey();
  const timestamp = Date.now();
  const data = password + ':' + timestamp;

  // 使用 jsencrypt 进行加密
  const encryptor = new JSEncrypt();
  encryptor.setPublicKey(publicKey); // 设置公钥
  const encryptedPassword = encryptor.encrypt(data); // 加密数据

  if (!encryptedPassword) {
    throw new Error('加密失败，请检查公钥格式是否正确');
  }

  // 将 Base64 编码的密文转换为字节数组
  const encryptedBytes = Buffer.from(encryptedPassword, 'base64');
  return encryptedBytes.toString('base64'); // 返回 Base64 编码的密文
};

// 登录
export const login = async (username, password) => {
  const encryptedPassword = await encryptPassword(password);
  const params = new URLSearchParams();
  params.append('username', username);
  params.append('password', encryptedPassword);
  // 设置cookie
  const response = await axiosInstance.post(endpoints.login, params, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  });
  
  return response.data;
};

// 注册
export const register = async (username, password) => {
  const encryptedPassword = await encryptPassword(password);
  const params = new URLSearchParams();
  params.append('username', username);
  params.append('password', encryptedPassword);
  const response = await axiosInstance.post(endpoints.signup, params, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  });
  return response.data;
};


// 刷新token
export const validateTokenAndGetNewAccessToken = async () => {
  const response = await axiosInstance.post('/account/refresh_token');
  return response.data;
};


// src/api/userService.js
import axiosInstance from './axiosInstance';

const userService = {
  hasUser(username) {
    return axiosInstance.get(`/users/exists?username=${username}`);
  },
  getUser(userId) {
    return axiosInstance.get(`/users/${userId}`);
  },
  createUser(userData) {
    return axiosInstance.post('/users', userData);
  },
  updateUser(userId, userData) {
    return axiosInstance.put(`/users/${userId}`, userData);
  },
  deleteUser(userId) {
    return axiosInstance.delete(`/users/${userId}`);
  },
  getAllUsers() {
    return axiosInstance.get('/users');
  }
};

export default userService;

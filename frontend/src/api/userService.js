// src/api/userService.js
import axiosInstance from './axiosInstance';

const userService = {
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
};

export default userService;

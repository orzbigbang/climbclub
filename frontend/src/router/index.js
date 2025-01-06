import { createRouter, createWebHistory } from 'vue-router'

import MainViewVue from '@/views/MainView.vue'
import HomeViewVue from '@/views/HomeView.vue'
import LoginViewVue from '@/views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "Main",
      component: MainViewVue
    },
    {
      path: "/login",
      name: "Login",
      component: LoginViewVue
    },
    {
      path: "/home",
      name: "Home",
      component: HomeViewVue
    },
  ],
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 };
  }
})

export default router

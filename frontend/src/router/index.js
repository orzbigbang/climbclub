import { createRouter, createWebHistory } from 'vue-router'
import { useAccountStore } from '@/stores/account'
import { routes } from '@/stores/navigation'

import HPViewVue from '@/views/HPView.vue'
import OauthViewVue from '@/views/OauthView.vue'
import HomeViewVue from '@/views/HomeView.vue'
import SupportViewVue from '@/views/SupportView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "HP",
      component: HPViewVue
    },
    {
      path: "/oauth",
      name: "Oauth",
      component: OauthViewVue,
      children: [
        {
          path: "login",
          name: "OauthLogin",
          query: {
            redirectUrl: routes.home
          },
          component: () => import('@/components/Oauth/OauthLogin.vue')
        },
        {
          path: "signup",
          name: "OauthSignup",
          component: () => import('@/components/Oauth/OauthSignup.vue'),
        }
      ],
      beforeEnter: async (to, from, next) => {
        const accountStore = useAccountStore()
        await accountStore.initializeAuth()
        
        if (accountStore.isLoggedIn) {
          next(routes.home);
        } else {
          next();
        }
      },
    },
    {
      path: "/home",
      name: "Home",
      component: HomeViewVue,
      beforeEnter: async (to, from, next) => {
        const accountStore = useAccountStore()
        await accountStore.initializeAuth()
        if (!accountStore.isLoggedIn) {
          next(routes.login);
        } else {
          next();
        }
      },
    },
    {
      path: "/support",
      name: "Support",
      component: SupportViewVue,
      // children: [
      //   {
      //     path: "faq",
      //     name: "SupportFaq",
      //     component: () => import('@/components/Support/SupportFaq.vue')
      //   },
      //   {
      //     path: "contact",
      //     name: "SupportContact",
      //     component: () => import('@/components/Support/SupportContact.vue')
      //   },
      //   {
      //     path: "agreement",
      //     name: "SupportAgreement",
      //     component: () => import('@/components/Support/SupportAgreement.vue')
      //   },
      //   {
      //     path: "privacy",
      //     name: "SupportPrivacy",
      //     component: () => import('@/components/Support/SupportPrivacy.vue')
      //   },
      //   {
      //     path: "feedback",
      //     name: "SupportFeedback",
      //     component: () => import('@/components/Support/SupportFeedback.vue')
      //   }
      // ]
    },
  ],
  scrollBehavior(to, from, savedPosition) {
    return { top: 0 };
  }
})

export default router

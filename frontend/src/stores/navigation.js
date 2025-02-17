import { defineStore } from 'pinia'
import { ref } from 'vue'

export const routes = {
  HP: '/',
  home: '/home',
  login: '/oauth/login',
  signup: '/oauth/signup',
  resetPassword: '/oauth/resetPassword',
  support: '/support',
}


export const useNavigationStore = defineStore('navigation', () => {
  const navigationTarget = ref({
    path: '',
    query: null
  })

  function navigate(path, query = null) {
    navigationTarget.value = {
      path,
      query
    }
  }

  function navigateLogin(redirectUrl = null) {
    if (redirectUrl) {
      navigationTarget.value = {
        path: routes.login,
        query: {redirectUrl},
      }
    } else {
      navigationTarget.value = {
        path: routes.login,
      }
    }
  }

  function navigateSignup(redirectUrl = null) {
    if (redirectUrl) {
      navigationTarget.value = {
        path: routes.signup,
        query: {redirectUrl},
      }
    } else {
      navigationTarget.value = {
        path: routes.signup,
      }
    }
  }

  function navigateHome() {
    navigationTarget.value = {
      path: routes.home,
    }
  }

  function navigateHP() {
    navigationTarget.value = {
      path: routes.HP,
    }
  }

  function navigateSupport() {
    navigationTarget.value = {
      path: routes.support,
    }
  }

  return {
    navigationTarget,
    navigate,
    navigateLogin,
    navigateSignup,
    navigateHome,
    navigateHP,
    navigateSupport,
  }
})
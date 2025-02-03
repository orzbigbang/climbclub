import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useShowStore = defineStore('show', () => {
  const notification = ref({
    show: false,
    message: '',
    type: 'success',
    duration: 3000
  })

  const showNotification = (message, type = 'success', duration = 3000, callback = null) => {
    notification.value = {
      show: true,
      message,
      type,
      duration
    }

    setTimeout(() => {
      notification.value.show = false
      if (callback) {
        callback()
      }
    }, duration)
  }

  const loading = ref(false)

  const showLoading = (waitFor, callback = null) => {
    loading.value = true
    
    waitFor.then(() => {
      loading.value = false
      if (callback) {
        callback()
      }
    }).catch(() => {
      loading.value = false
    })
  }

  return {
    notification,
    showNotification,
    loading,
    showLoading
  }
})
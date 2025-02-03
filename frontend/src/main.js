import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { getBrowserFingerprint } from './api/browser'

import App from './App.vue'
import router from './router'
const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')

// 获取浏览器指纹
getBrowserFingerprint()

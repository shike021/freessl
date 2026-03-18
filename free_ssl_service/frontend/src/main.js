import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from 'axios'

const app = createApp(App)

app.config.productionTip = false

app.use(ElementPlus)

axios.defaults.baseURL = process.env.VUE_APP_API_BASE_URL || 'http://localhost:3000/api'
app.config.globalProperties.$http = axios

app.use(router)
app.use(store)

app.mount('#app')

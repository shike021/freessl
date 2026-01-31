import axios from 'axios'
import { Message } from 'element-ui'

// Create axios instance with base URL
const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:5000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor to add auth token
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  response => {
    return response
  },
  error => {
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 401:
          Message.error('未授权，请重新登录')
          localStorage.removeItem('token')
          window.location.href = '/login'
          break
        case 403:
          Message.error('没有权限访问此资源')
          break
        case 404:
          Message.error('请求的资源不存在')
          break
        case 500:
          Message.error('服务器错误，请稍后重试')
          break
        default:
          Message.error(data.error || '请求失败')
      }
    } else if (error.request) {
      Message.error('网络错误，请检查网络连接')
    } else {
      Message.error('请求配置错误')
    }
    
    return Promise.reject(error)
  }
)

export default api
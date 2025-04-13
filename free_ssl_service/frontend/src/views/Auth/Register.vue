<template>
  <div class="register-container">
    <el-card class="register-box">
      <h2>注册</h2>
      
      <el-form ref="form" :model="form" :rules="rules" @submit.native.prevent="register">
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="用户名 (至少3个字符)"
            prefix-icon="el-icon-user"
          />
        </el-form-item>
        
        <el-form-item prop="email">
          <el-input
            v-model="form.email"
            placeholder="邮箱地址"
            prefix-icon="el-icon-message"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码 (至少8个字符，包含字母和数字)"
            prefix-icon="el-icon-lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item prop="confirmPassword">
          <el-input
            v-model="form.confirmPassword"
            type="password"
            placeholder="确认密码"
            prefix-icon="el-icon-lock"
            show-password
          />
        </el-form-item>
        
      <el-form-item>
        <el-button
          type="primary"
          native-type="submit"
          :loading="loading"
          class="register-btn"
        >
          手动注册
        </el-button>
        <el-button
          type="success"
          @click="oauthRegister('google')"
          class="oauth-google-btn"
        >
          使用Google注册
        </el-button>
        <el-button
          type="info"
          @click="oauthRegister('wechat')"
          class="oauth-wechat-btn"
        >
          使用微信注册
        </el-button>
        </el-form-item>
      </el-form>
      
      <div class="links">
        <router-link to="/login">已有账号？登录</router-link>
      </div>
    </el-card>
  </div>
</template>
<script>
import { mapActions } from 'vuex'

export default {
  data() {
    const validatePassword = (rule, value, callback) => {
      if (value !== this.form.password) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    }
    
    return {
      form: {
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 50, message: '用户名长度应在3到50个字符之间', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 8, message: '密码长度至少为8个字符', trigger: 'blur' },
          { pattern: /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/, message: '密码必须包含字母和数字', trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, message: '请再次输入密码', trigger: 'blur' },
          { validator: validatePassword, trigger: 'blur' }
        ]
      },
      loading: false
    }
  },
  methods: {
    ...mapActions('auth', ['register']),
    
    async register() {
      this.$refs.form.validate(async valid => {
        if (valid) {
          this.loading = true
          try {
            await this.$store.dispatch('auth/register', this.form)
            this.$message.success('注册成功，请检查您的邮箱进行验证')
            this.$router.push('/login')
          } catch (error) {
            this.$message.error(
              error.response?.data?.error || '注册失败，请重试'
            )
          } finally {
            this.loading = false
          }
        }
      })
    },
    
    oauthRegister(provider) {
      window.location.href = `${process.env.VUE_APP_API_BASE_URL}/auth/login/${provider}`
      this.$refs.form.validate(async valid => {
        if (valid) {
          this.loading = true
          try {
            await this.$store.dispatch('auth/register', this.form)
            this.$message.success('注册成功，请检查您的邮箱进行验证')
            this.$router.push('/login')
          } catch (error) {
            this.$message.error(
              error.response?.data?.error || '注册失败，请重试'
            )
          } finally {
            this.loading = false
          }
        }
      })
    }
  }
}
</script>
<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #ffe0b2; /* 浅橙色 */
}

.register-box {
  width: 400px;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #ff5722; /* 深橙色 */
}

.register-btn {
  width: 100%;
  background-color: #ff9800; /* 主色调橙色 */
  border-color: #ff9800;
}

.register-btn:hover {
  background-color: #fb8c00; /* 稍深的橙色 */
  border-color: #fb8c00;
}

.oauth-google-btn {
  width: 100%;
  margin-top: 10px;
  background-color: #dd2c00; /* Google风格红色 */
  border-color: #dd2c00;
}

.oauth-google-btn:hover {
  background-color: #c42600; /* 稍深的红色 */
  border-color: #c42600;
}

.oauth-wechat-btn {
  width: 100%;
  margin-top: 10px;
  background-color: #00c853; /* 微信风格绿色 */
  border-color: #00c853;
}

.oauth-wechat-btn:hover {
  background-color: #00b24d; /* 稍深的绿色 */
  border-color: #00b24d;
}

.links {
  display: flex;
  justify-content: center;
  margin-top: 15px;
  font-size: 14px;
}

a {
  color: #ff9800; /* 主色调橙色 */
  text-decoration: none;
}

a:hover {
  color: #e65100; /* 稍深的橙色 */
  text-decoration: underline;
}
</style>

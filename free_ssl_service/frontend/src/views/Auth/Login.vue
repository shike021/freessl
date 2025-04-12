<template>
  <div class="login-container">
    <el-card class="login-box">
      <h2>登录</h2>
      
      <el-form ref="form" :model="form" :rules="rules" @submit.native.prevent="login">
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="用户名"
            prefix-icon="el-icon-user"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码"
            prefix-icon="el-icon-lock"
            show-password
          />
        </el-form-item>
        
      <el-form-item>
        <el-button
          type="primary"
          native-type="submit"
          :loading="loading"
          class="login-btn"
        >
          手动登录
        </el-button>
        <el-button
          type="success"
          @click="oauthLogin('google')"
          class="oauth-google-btn"
        >
          使用Google登录
        </el-button>
        <el-button
          type="info"
          @click="oauthLogin('wechat')"
          class="oauth-wechat-btn"
        >
          使用微信登录
        </el-button>
        </el-form-item>
      </el-form>
      
      <div class="links">
        <router-link to="/register">注册新账号</router-link>
        <router-link to="/forgot-password">忘记密码?</router-link>
      </div>
    </el-card>
  </div>
</template>
<script>
import { mapActions } from 'vuex'

export default {
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      },
      loading: false
    }
  },
  methods: {
    ...mapActions('auth', ['login']),
    
    async login() {
      this.$refs.form.validate(async valid => {
        if (valid) {
          this.loading = true
          try {
            await this.$store.dispatch('auth/login', this.form)
            this.$router.push('/dashboard')
          } catch (error) {
            this.$message.error(
              error.response?.data?.error || '登录失败，请重试'
            )
          } finally {
            this.loading = false
          }
        }
      })
    },
    
    oauthLogin(provider) {
      window.location.href = `${process.env.VUE_APP_API_BASE_URL}/auth/login/${provider}`
      this.$refs.form.validate(async valid => {
        if (valid) {
          this.loading = true
          try {
            await this.$store.dispatch('auth/login', this.form)
            this.$router.push('/dashboard')
          } catch (error) {
            this.$message.error(
              error.response?.data?.error || '登录失败，请重试'
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
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f5f7fa;
}

.login-box {
  width: 400px;
  padding: 20px;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #303133;
}

.login-btn {
  width: 100%;
}

.links {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
  font-size: 14px;
}

a {
  color: #409eff;
  text-decoration: none;
}
</style>

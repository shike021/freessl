<template>
  <div class="forgot-password">
    <el-card class="forgot-password-card">
      <h1>忘记密码</h1>
      
      <el-form ref="form" :model="form" :rules="rules" @submit.native.prevent="sendResetLink">
        <el-form-item prop="email">
          <el-input
            v-model="form.email"
            placeholder="请输入您的邮箱地址"
            prefix-icon="el-icon-message"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            native-type="submit"
            :loading="loading"
            class="reset-btn"
          >
            发送重置链接
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'ForgotPassword',
  data() {
    return {
      form: {
        email: ''
      },
      rules: {
        email: [
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
        ]
      },
      loading: false
    }
  },
  methods: {
    async sendResetLink() {
      this.$refs.form.validate(async valid => {
        if (valid) {
          this.loading = true
          try {
            await this.$store.dispatch('auth/sendResetLink', this.form.email)
            this.$message.success('重置链接已发送，请检查您的邮箱')
          } catch (error) {
            this.$message.error('发送失败: ' + (error.response?.data?.message || error.message))
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
.forgot-password {
  padding: 40px;
  background-color: #ffe0b2; /* 浅橙色 */
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.forgot-password-card {
  width: 400px;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
  color: #ff5722; /* 深橙色 */
}

.reset-btn {
  width: 100%;
  background-color: #ff9800; /* 主色调橙色 */
  border-color: #ff9800;
}

.reset-btn:hover {
  background-color: #fb8c00; /* 稍深的橙色 */
  border-color: #fb8c00;
}
</style>

<template>
  <div class="reset-password">
    <el-card class="reset-password-card">
      <h1>重置密码</h1>
      
      <el-form ref="form" :model="form" :rules="rules" @submit.native.prevent="resetPassword">
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入新密码"
            prefix-icon="el-icon-lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item prop="confirmPassword">
          <el-input
            v-model="form.confirmPassword"
            type="password"
            placeholder="请再次输入新密码"
            prefix-icon="el-icon-lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            native-type="submit"
            :loading="loading"
            class="reset-btn"
          >
            重置密码
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'ResetPassword',
  data() {
    const validateConfirmPassword = (rule, value, callback) => {
      if (value !== this.form.password) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    }
    
    return {
      form: {
        password: '',
        confirmPassword: ''
      },
      rules: {
        password: [
          { required: true, message: '请输入新密码', trigger: 'blur' },
          { min: 8, message: '密码长度至少为8个字符', trigger: 'blur' },
          { pattern: /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/, message: '密码必须包含字母和数字', trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, message: '请再次输入新密码', trigger: 'blur' },
          { validator: validateConfirmPassword, trigger: 'blur' }
        ]
      },
      loading: false
    }
  },
  methods: {
    async resetPassword() {
      this.$refs.form.validate(async valid => {
        if (valid) {
          this.loading = true
          try {
            const token = this.$route.query.token
            await this.$store.dispatch('auth/resetPassword', { token, password: this.form.password })
            this.$message.success('密码重置成功，请登录')
            this.$router.push('/login')
          } catch (error) {
            this.$message.error('重置失败: ' + (error.response?.data?.message || error.message))
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
.reset-password {
  padding: 40px;
  background-color: #ffe0b2; /* 浅橙色 */
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.reset-password-card {
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

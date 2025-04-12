<template>
  <div class="forgot-password-container">
    <el-card class="forgot-password-box">
      <h2>忘记密码</h2>
      
      <el-form ref="form" :model="form" :rules="rules" @submit.native.prevent="submit">
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
            class="submit-btn"
          >
            提交
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>
<script>
import { mapActions } from 'vuex'

export default {
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
    ...mapActions('auth', ['forgotPassword']),
    
    async submit() {
      this.$refs.form.validate(async valid => {
        if (valid) {
          this.loading = true
          try {
            await this.forgotPassword(this.form.email)
            this.$message.success('重置链接已发送，请检查您的邮箱')
          } catch (error) {
            this.$message.error('操作失败: ' + (error.response?.data?.message || error.message))
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
.forgot-password-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f5f7fa;
}

.forgot-password-box {
  width: 400px;
  padding: 20px;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #303133;
}

.submit-btn {
  width: 100%;
}
</style>

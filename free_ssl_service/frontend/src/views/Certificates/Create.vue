<template>
  <div class="certificate-create">
    <el-card>
      <h2>申请新证书</h2>
      
      <el-form ref="form" :model="form" :rules="rules" @submit.native.prevent="createCertificate">
        <el-form-item prop="domains">
          <el-input
            v-model="form.domains"
            placeholder="输入域名,多个用逗号分隔"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            native-type="submit"
            :loading="loading"
            class="create-btn"
          >
            申请证书
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
        domains: ''
      },
      rules: {
        domains: [
          { required: true, message: '请输入域名', trigger: 'blur' }
        ]
      },
      loading: false
    }
  },
  methods: {
    ...mapActions('certs', ['createCertificate']),
    
    async createCertificate() {
      this.$refs.form.validate(async valid => {
        if (valid) {
          this.loading = true
          try {
            await this.createCertificate(this.form)
            this.$message.success('证书申请成功')
            this.$router.push('/certificates')
          } catch (error) {
            this.$message.error('申请失败: ' + (error.response?.data?.message || error.message))
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
.certificate-create {
  padding: 20px;
}

.create-btn {
  width: 100%;
}
</style>

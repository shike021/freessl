<template>
  <div class="certificate-renew">
    <el-card>
      <h2>续期证书</h2>
      
      <el-form ref="form" :model="form" :rules="rules" @submit.native.prevent="renewCertificate">
        <el-form-item prop="paymentMethod">
          <el-select v-model="form.paymentMethod" placeholder="选择支付方式">
            <el-option label="信用卡" value="credit_card"></el-option>
            <el-option label="PayPal" value="paypal"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            native-type="submit"
            :loading="loading"
            class="renew-btn"
          >
            续期证书
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
        paymentMethod: ''
      },
      rules: {
        paymentMethod: [
          { required: true, message: '请选择支付方式', trigger: 'change' }
        ]
      },
      loading: false
    }
  },
  methods: {
    ...mapActions('certs', ['renewCertificate']),
    
    async renewCertificate() {
      this.$refs.form.validate(async valid => {
        if (valid) {
          this.loading = true
          try {
            const certId = this.$route.params.id
            await this.renewCertificate({ id: certId, data: this.form })
            this.$message.success('证书续期成功')
            this.$router.push('/certificates')
          } catch (error) {
            this.$message.error('续期失败: ' + (error.response?.data?.message || error.message))
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
.certificate-renew {
  padding: 40px;
  background-color: #ffe0b2; /* 浅橙色 */
}

.el-card {
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #ff5722; /* 深橙色 */
}

.renew-btn {
  width: 100%;
  background-color: #ff9800; /* 主色调橙色 */
  border-color: #ff9800;
}

.renew-btn:hover {
  background-color: #fb8c00; /* 稍深的橙色 */
  border-color: #fb8c00;
}
</style>

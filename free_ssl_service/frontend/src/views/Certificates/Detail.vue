<template>
  <div class="certificate-detail">
    <el-card>
      <h2>证书详情</h2>
      
      <el-row :gutter="20" class="mb-20">
        <el-col :span="8">域名:</el-col>
        <el-col :span="16">{{ certificate.domains }}</el-col>
      </el-row>
      
      <el-row :gutter="20" class="mb-20">
        <el-col :span="8">申请日期:</el-col>
        <el-col :span="16">{{ formatDate(certificate.issue_date) }}</el-col>
      </el-row>
      
      <el-row :gutter="20" class="mb-20">
        <el-col :span="8">过期日期:</el-col>
        <el-col :span="16">
          <span :class="{'text-danger': isExpired(certificate.expiry_date)}">
            {{ formatDate(certificate.expiry_date) }}
          </span>
        </el-col>
      </el-row>
      
      <el-row :gutter="20" class="mb-20">
        <el-col :span="8">状态:</el-col>
        <el-col :span="16">
          <el-tag
            :type="getStatusType(certificate.status)"
            size="small"
          >
            {{ certificate.status === 'active' ? '有效' : '已过期' }}
          </el-tag>
        </el-col>
      </el-row>
      
      <el-row :gutter="20" class="mb-20" v-if="certificate.can_renew">
        <el-col :span="24">
          <el-button type="primary" @click="renewCertificate">
            续期证书
          </el-button>
        </el-col>
      </el-row>
      
      <el-tabs v-model="activeTab" class="mt-20">
        <el-tab-pane label="证书" name="certificate">
          <pre>{{ certificate.certificate }}</pre>
        </el-tab-pane>
        <el-tab-pane label="私钥" name="privateKey">
          <pre>{{ certificate.private_key }}</pre>
        </el-tab-pane>
        <el-tab-pane label="链" name="chain">
          <pre>{{ certificate.chain }}</pre>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>
<script>
import { mapActions } from 'vuex'

export default {
  data() {
    return {
      certificate: {},
      activeTab: 'certificate',
      loading: false
    }
  },
  created() {
    this.loadCertificate()
  },
  methods: {
    ...mapActions('certs', ['fetchCertificate', 'renew']),
    
    async loadCertificate() {
      this.loading = true
      try {
        const certId = this.$route.params.id
        const response = await this.fetchCertificate(certId)
        this.certificate = response.data
      } catch (error) {
        this.$message.error('加载证书失败: ' + (error.response?.data?.message || error.message))
      } finally {
        this.loading = false
      }
    },
    
    async renewCertificate() {
      try {
        const certId = this.$route.params.id
        await this.renew({ id: certId })
        this.$message.success('证书续期成功')
        this.loadCertificate()
      } catch (error) {
        this.$message.error('续期失败: ' + (error.response?.data?.message || error.message))
      }
    },
    
    formatDate(date) {
      return new Date(date).toLocaleDateString()
    },
    
    isExpired(expiryDate) {
      return new Date(expiryDate) < new Date()
    },
    
    getStatusType(status) {
      return status === 'active' ? 'success' : 'danger'
    }
  }
}
</script>
<style scoped>
.certificate-detail {
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

.mb-20 {
  margin-bottom: 20px;
}

.mt-20 {
  margin-top: 20px;
}

.text-danger {
  color: #e65100; /* 深橙色 */
}

.el-button {
  width: 100%;
  background-color: #ff9800; /* 主色调橙色 */
  border-color: #ff9800;
}

.el-button:hover {
  background-color: #fb8c00; /* 稍深的橙色 */
  border-color: #fb8c00;
}
</style>

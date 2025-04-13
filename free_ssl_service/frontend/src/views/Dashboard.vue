<template>
  <div class="dashboard">
    <el-row :gutter="20" class="mb-20">
      <el-col :span="12">
        <el-card class="summary-card">
          <h3>证书概览</h3>
          <p>有效证书: {{ validCertificatesCount }}</p>
          <p>即将到期: {{ expiringCertificatesCount }}</p>
          <p>已过期: {{ expiredCertificatesCount }}</p>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card class="summary-card">
          <h3>用户信息</h3>
          <p>用户名: {{ user.username }}</p>
          <p>邮箱: {{ user.email }}</p>
        </el-card>
      </el-col>
    </el-row>
    
    <el-card class="recent-activity">
      <h3>最近活动</h3>
      <el-table :data="recentCertificates" v-loading="loading">
        <el-table-column prop="domains" label="域名" min-width="200"></el-table-column>
        <el-table-column prop="issue_date" label="申请日期" width="150">
          <template #default="{ row }">
            {{ formatDate(row.issue_date) }}
          </template>
        </el-table-column>
        <el-table-column prop="expiry_date" label="过期日期" width="150">
          <template #default="{ row }">
            <span :class="{'text-danger': isExpired(row.expiry_date)}">
              {{ formatDate(row.expiry_date) }}
            </span>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>
<script>
import { mapState, mapActions } from 'vuex'

export default {
  data() {
    return {
      loading: false
    }
  },
  computed: {
    ...mapState('auth', ['user']),
    ...mapState('certs', ['certificates']),
    validCertificatesCount() {
      return this.certificates.filter(cert => !this.isExpired(cert.expiry_date)).length
    },
    expiringCertificatesCount() {
      const now = new Date()
      const threshold = new Date(now.setDate(now.getDate() + 30))
      return this.certificates.filter(cert =>
        new Date(cert.expiry_date) > now && new Date(cert.expiry_date) <= threshold
      ).length
    },
    expiredCertificatesCount() {
      return this.certificates.filter(cert => this.isExpired(cert.expiry_date)).length
    },
    recentCertificates() {
      return [...this.certificates].sort((a, b) => new Date(b.issue_date) - new Date(a.issue_date)).slice(0, 5)
    }
  },
  created() {
    this.loadCertificates()
  },
  methods: {
    ...mapActions('certs', ['fetchCertificates']),
    
    async loadCertificates() {
      this.loading = true
      try {
        await this.fetchCertificates()
      } catch (error) {
        this.$message.error('加载证书失败: ' + (error.response?.data?.message || error.message))
      } finally {
        this.loading = false
      }
    },
    
    formatDate(date) {
      return new Date(date).toLocaleDateString()
    },
    
    isExpired(expiryDate) {
      return new Date(expiryDate) < new Date()
    }
  }
}
</script>
<style scoped>
.dashboard {
  padding: 20px;
  background-color: #ffe0b2; /* 浅橙色 */
}

.mb-20 {
  margin-bottom: 20px;
}

.summary-card {
  height: 150px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

.recent-activity {
  margin-top: 20px;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

.text-danger {
  color: #e65100; /* 深橙色 */
}
</style>

<template>
  <div class="certificate-list">
    <el-row justify="space-between" align="middle" class="mb-20">
      <el-col :span="12">
        <h2>我的SSL证书</h2>
      </el-col>
      <el-col :span="12" class="text-right">
        <el-button
          type="primary"
          icon="el-icon-plus"
          @click="$router.push('/certificates/create')"
        >
          申请新证书
        </el-button>
      </el-col>
    </el-row>
    
    <el-table :data="certificates" v-loading="loading">
      <el-table-column prop="domains" label="域名" min-width="200">
        <template #default="{ row }">
          <router-link :to="`/certificates/${row.id}`">
            {{ row.domains }}
          </router-link>
        </template>
      </el-table-column>
      
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
      
      <el-table-column prop="status" label="状态" width="120">
        <template #default="{ row }">
          <el-tag
            :type="getStatusType(row.status)"
            size="small"
          >
            {{ row.status === 'active' ? '有效' : '已过期' }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button
            size="mini"
            @click="$router.push(`/certificates/${row.id}/renew`)"
            v-if="row.can_renew"
          >
            续期
          </el-button>
          <el-button
            size="mini"
            @click="$router.push(`/certificates/${row.id}`)"
          >
            详情
          </el-button>
        </template>
      </el-table-column>
    </el-table>
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
    ...mapState('certs', ['certificates'])
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
    },
    
    getStatusType(status) {
      return status === 'active' ? 'success' : 'danger'
    }
  }
}
</script>
<style scoped>
.certificate-list {
  padding: 20px;
  background-color: #ffe0b2; /* 浅橙色 */
}

.mb-20 {
  margin-bottom: 20px;
}

.text-right {
  text-align: right;
}

.text-danger {
  color: #e65100; /* 深橙色 */
}

.el-table {
  border-radius: 8px;
  overflow: hidden;
}

.el-button--mini {
  background-color: #ff9800; /* 主色调橙色 */
  border-color: #ff9800;
}

.el-button--mini:hover {
  background-color: #fb8c00; /* 稍深的橙色 */
  border-color: #fb8c00;
}

.el-tag--success {
  background-color: #cddc39; /* 成功状态绿色 */
}

.el-tag--danger {
  background-color: #e65100; /* 失败状态深橙色 */
}
</style>

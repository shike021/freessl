<template>
  <el-header class="navbar">
    <el-row align="middle">
      <el-col :span="12">
        <router-link to="/dashboard" class="logo">
          SSL证书服务
        </router-link>
      </el-col>
      
      <el-col :span="12">
        <el-dropdown v-if="user" @command="handleCommand">
          <span class="el-dropdown-link">
            <el-avatar :size="30" :src="user.avatar || ''" class="mr-10" />
            {{ user.username }}
            <i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item command="profile">个人资料</el-dropdown-item>
            <el-dropdown-item command="logout">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
        
        <div v-else>
          <router-link to="/login" class="login-btn">登录</router-link>
          <router-link to="/register" class="register-btn">注册</router-link>
        </div>
      </el-col>
    </el-row>
  </el-header>
</template>
<script>
import { mapState, mapActions } from 'vuex'

export default {
  computed: {
    ...mapState('auth', ['user'])
  },
  methods: {
    ...mapActions('auth', ['logout']),
    
    handleCommand(command) {
      if (command === 'logout') {
        this.logout()
        this.$router.push('/login')
      } else if (command === 'profile') {
        this.$router.push('/profile')
      }
    }
  }
}
</script>
<style scoped>
.navbar {
  background: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  line-height: 60px;
}

.logo {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
  text-decoration: none;
}

.login-btn, .register-btn {
  padding: 0 15px;
  color: #606266;
  text-decoration: none;
}

.register-btn {
  color: #409eff;
}

.mr-10 {
  margin-right: 10px;
}

.el-dropdown-link {
  cursor: pointer;
}
</style>

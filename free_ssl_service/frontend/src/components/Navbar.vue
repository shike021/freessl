<template>
  <nav class="navbar">
    <div class="container">
      <router-link to="/" class="navbar-brand">
        Free SSL Service
      </router-link>
      
      <ul class="navbar-nav">
        <li class="nav-item">
          <router-link to="/certificates" class="nav-link">证书管理</router-link>
        </li>
        <li class="nav-item" v-if="isAuthenticated">
          <router-link to="/profile" class="nav-link">个人中心</router-link>
        </li>
        <li class="nav-item" v-if="!isAuthenticated">
          <router-link to="/login" class="nav-link">登录</router-link>
        </li>
        <li class="nav-item" v-if="!isAuthenticated">
          <router-link to="/register" class="nav-link">注册</router-link>
        </li>
        <li class="nav-item" v-if="isAuthenticated">
          <a href="#" @click.prevent="logout" class="nav-link">退出登录</a>
        </li>
      </ul>
    </div>
  </nav>
</template>
<script>
export default {
  data() {
    return {
      activeIndex: '1',
      isAuthenticated: false
    }
  },
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath)
    },
    logout() {
      // ...原来的登出逻辑
    }
  }
}
</script>
<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: var(--primary-color);
  color: white;
}

.navbar-brand {
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
  color: white;
}

.navbar-nav {
  display: flex;
  gap: 1rem;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-size: 1rem;
}

.nav-link:hover {
  text-decoration: underline;
}
</style>

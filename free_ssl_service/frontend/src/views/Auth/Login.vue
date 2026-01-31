<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2>登录您的账号</h2>
      <form @submit.prevent="login">
        <div class="form-group">
          <label for="email">电子邮箱</label>
          <input id="email" v-model="email" type="email" required>
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input id="password" v-model="password" type="password" required>
        </div>
        <div class="button-group">
          <button type="submit" class="button primary-button">登录</button>
          <router-link to="/register" class="button secondary-button">注册新账号</router-link>
          <router-link to="/forgot-password" class="button tertiary-button">忘记密码</router-link>
        </div>
      </form>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    login() {
      // ...原来的登录逻辑
    }
  }
}
</script>
<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100%;
  padding: 2rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.auth-card {
  background: white;
  padding: 3rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h2 {
  color: var(--primary-color);
  margin-bottom: 1.5rem;
  text-align: center;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
}

.button {
  flex: 1;
  margin: 0 0.5rem;
}

.button {
  width: 100%;
  text-align: center;
  text-decoration: none;
}

.button:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>

<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2>注册新账号</h2>
      <form @submit.prevent="register">
        <div class="form-group">
          <label for="email">电子邮箱</label>
          <input id="email" v-model="email" type="email" required>
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input id="password" v-model="password" type="password" required>
        </div>
        <div class="form-group">
          <label for="confirm-password">确认密码</label>
          <input id="confirm-password" v-model="confirmPassword" type="password" required>
        </div>
        <div class="button-group">
          <button type="submit" class="button primary-button">注册</button>
          <router-link to="/login" class="button secondary-button">已有账号？登录</router-link>
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
      password: '',
      confirmPassword: ''
    }
  },
  methods: {
    register() {
      // ...原来的注册逻辑
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
  flex-direction: column;
  gap: 1rem;
  margin-top: 2rem;
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

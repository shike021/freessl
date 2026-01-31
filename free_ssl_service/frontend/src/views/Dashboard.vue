<template>
  <div class="auth-container">
    <section class="hero-section">
      <div class="hero-content">
        <h1>免费的SSL证书服务</h1>
        <p>为您的网站提供安全、可靠的HTTPS加密，完全免费</p>
        <router-link to="/certificates/create" class="button primary-button">
          立即获取SSL证书
        </router-link>
      </div>
    </section>

    <section class="features-section">
      <div class="feature">
        <h3><i class="fas fa-lock"></i> 安全可靠</h3>
        <p>采用行业标准的256位加密，确保数据传输安全</p>
      </div>
      <div class="feature">
        <h3><i class="fas fa-sync-alt"></i> 自动续期</h3>
        <p>90天有效期到期自动提醒，轻松续期保障服务不中断</p>
      </div>
      <div class="feature">
        <h3><i class="fas fa-headset"></i> 专业支持</h3>
        <p>遇到任何问题，我们的专业团队随时为您提供帮助</p>
      </div>
    </section>

    <section class="testimonials">
      <h2>用户评价</h2>
      <div class="testimonial-cards">
        <blockquote>
          <p>"使用Free SSL服务让我们的网站在短时间内就获得了安全认证，流程非常简单！"</p>
          <cite>- 张小伟, Tech Startup CEO</cite>
        </blockquote>
        <blockquote>
          <p>"作为个人博客主，找到完全免费的SSL服务真的省去了很多烦恼。"</p>
          <cite>- 李华, Personal Blogger</cite>
        </blockquote>
      </div>
    </section>
  </div>
</template>
<script>
export default {
  name: 'Dashboard'
}
</script>
<style scoped>
.auth-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.hero-section {
  background: linear-gradient(135deg, var(--secondary-color) 0%, var(--primary-color) 100%);
  color: white;
  padding: 5rem 2rem;
  border-radius: 8px;
  margin-bottom: 3rem;
  text-align: center;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-content h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.hero-content p {
  font-size: 1.25rem;
  margin-bottom: 2rem;
}

.features-section {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  margin-bottom: 3rem;
}

.feature {
  flex: 1 1 300px;
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.feature i {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: var(--secondary-color);
}

.testimonials {
  margin-top: 3rem;
}

.testimonials h2 {
  text-align: center;
  margin-bottom: 2rem;
}

.testimonial-cards {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
}

blockquote {
  flex: 1 1 300px;
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-left: 4px solid var(--secondary-color);
}

cite {
  display: block;
  margin-top: 1rem;
  font-style: normal;
  color: var(--secondary-color);
}
</style>

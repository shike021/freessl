<template>
  <div id="app">
    <Navbar />
    <router-view />
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue'

export default {
  components: {
    Navbar
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #333;
  background-color: #ff9800; /* 主色调橙色 */
  padding: 20px;
  min-height: 100%;
  display: flex;
  flex-direction: column;
}

body {
  margin: 0;
  padding: 0;
  background-color: #ff9800; /* 主色调橙色 */
}

html, body, #app {
  height: 100%;
}

body {
  margin: 0;
  padding: 0;
}

html, body, #app {
  height: 100%;
}
</style>

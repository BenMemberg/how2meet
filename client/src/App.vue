<script setup lang="ts">
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import { ref } from 'vue'

const app_title = "How2Meet"


</script>

<template>
  <header>
    <h1>{{ app_title }}</h1>
  </header>

  <nav>
    <RouterLink to="/">Go to Home</RouterLink>
    <RouterLink to="/about">Go to About</RouterLink>
  </nav>

  <main>
    <RouterView />
  </main>

  <footer>
  </footer>

</template>

<style scoped>
header {
  color: #000
}


</style>

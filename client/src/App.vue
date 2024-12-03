<script setup lang="ts">
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import { ref } from 'vue'

import home from './views/home.vue'

const app_title = "How2Meet"


</script>

<template>
  <header>
    <h1>{{ app_title }}</h1>
    <home />
  </header>


  <main>
  </main>

  <footer>
  </footer>

</template>

<style scoped>
header {
  color: #000
}


</style>

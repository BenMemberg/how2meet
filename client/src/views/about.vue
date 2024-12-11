<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'

const view_title = "About"

const router = useRouter()
const route = useRoute()

function goToHome() {
  router.push({
    name: 'home',
  })
}
</script>

<template>
  <h2>{{ view_title }}</h2>
  <div>Welcome to How2Meet! How2Meet is a frictionless event manager--meaning it is simple, free, easy to use, and does NOT require you or your guests to: Create an account or Download an app
</div>
  <button @click="goToHome">Go to Home</button>


</template>

<style scoped>

</style>

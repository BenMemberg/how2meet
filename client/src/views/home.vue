<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'

const view_title = "Home"

const router = useRouter()
const route = useRoute()

function goToAbout() {
  router.push({
    name: 'about',
  })
}

</script>

<template>
  <h2>{{ view_title }}</h2>
  <div>You are home. Be at peace.</div>
  <button @click="goToAbout">Go to About</button>

</template>

<style scoped>

</style>

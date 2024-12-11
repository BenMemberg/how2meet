import { createRouter, createWebHistory } from 'vue-router'
import home from "@/views/home.vue";
import about from "@/views/about.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: home
    },
    {
      path: '/about',
      name: 'about',
      component: about
    }
  ]
});

export default router;

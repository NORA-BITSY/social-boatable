import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/components/Feed.vue'
import ServicesPage from '@/components/ServicesListing.vue'
import LoginPage from '@/components/Login.vue'

const routes = [
  { path: '/', component: HomePage },
  { path: '/services', component: ServicesPage },
  { path: '/login', component: LoginPage },
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})

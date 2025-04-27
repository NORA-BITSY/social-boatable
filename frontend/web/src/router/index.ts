import { createRouter, createWebHistory } from 'vue-router'

import HomePage     from '@/components/Feed.vue'
import ServicesPage from '@/components/ServicesListing.vue'
import LoginPage    from '@/components/Login.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/',         name: 'home',     component: HomePage },
    { path: '/services', name: 'services', component: ServicesPage },
    { path: '/login',    name: 'login',    component: LoginPage },
  ],
})

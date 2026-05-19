import { createRouter, createWebHistory } from 'vue-router'
import StaffingView from '@/views/StaffingView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/dashboard' },
    { path: '/dashboard', component: () => import('@/views/DashboardView.vue') },
    { path: '/search', component: () => import('@/views/SearchView.vue') },
    { path: '/staffing', component: StaffingView },
    { path: '/employees', component: () => import('@/views/EmployeeView.vue') },
    { path: '/projects', component: () => import('@/views/ProjectView.vue') },
    { path: '/clients', component: () => import('@/views/ClientView.vue') },
    { path: '/assignments', component: () => import('@/views/AssignmentView.vue') },
  ],
})

export default router

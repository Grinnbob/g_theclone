import Vue from 'vue'
import VueRouter from 'vue-router'

const DashboardLayout = () => import('@/containers/DashboardLayout.vue')

const Users = () => import('@/views/Users.vue')
const Accounts = () => import('@/views/Accounts.vue')

let dashboardView = {
  path: '/',
  name: 'Dashboard',
  component: DashboardLayout
}

let users = {
  path: '/',
  component: DashboardLayout,
  children: [
    {
      path: 'users',
      name: 'Users',
      component: Users
    },
  ]
}

let accounts = {
  path: '/',
  component: DashboardLayout,
  children: [
    {
      path: 'accounts',
      name: 'Accounts',
      component: Accounts
    },
  ]
}

Vue.use(VueRouter)
const routes = [
  dashboardView,
  users,
  accounts
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router

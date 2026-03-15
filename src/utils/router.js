import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import MainPage from '../views/MainPage.vue'
import AdminPage from '../views/AdminPage.vue'

const routes = [
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { 
    path: '/main', 
    component: MainPage, 
    meta: { requiresAuth: true, role: 'user' } 
  },
  { 
    path: '/admin', 
    component: AdminPage, 
    meta: { requiresAuth: true, role: 'admin' } 
  },
  { path: '/', redirect: '/login' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const userRole = localStorage.getItem('role') // 'admin' или 'user'

  // Если страница требует авторизации
  if (to.meta.requiresAuth) {
    if (!token) {
      return next('/login')
    }
    // Проверка роли: если роль в маршруте не совпадает с ролью юзера
    if (to.meta.role && to.meta.role !== userRole) {
      // Отправляем туда, куда ему положено по роли
      return next(userRole === 'admin' ? '/admin' : '/user')
    }
  }
  next()
})

export default router
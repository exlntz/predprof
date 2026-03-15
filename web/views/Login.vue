<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const form = reactive({ username: '', password: '' })

const handleLogin = async () => {
  // Запрос к FastAPI...
  // Допустим, получили: { token: '...', role: 'admin' }
  const res = { token: 'xyz', role: 'admin' } 
  
  localStorage.setItem('token', res.token)
  localStorage.setItem('role', res.role)

  if (res.role === 'admin') {
    router.push('/admin')
  } else {
    router.push('/user')
  }
}
</script>


<template>
    <div class="auth-wrapper">
      <div class="auth-box">
        <h2>Система классификации 2226</h2>
        <form @submit.prevent="handleLogin">
          <input v-model="form.username" type="text" placeholder="Логин" required />
          <input v-model="form.password" type="password" placeholder="Пароль" required />
          <button type="submit">Идентифицироваться</button>
        </form>
        <router-link to="/register">Регистрация нового инженера</router-link>
      </div>
    </div>
  </template>
  

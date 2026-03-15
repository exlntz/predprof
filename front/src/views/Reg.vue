<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { advancedApiRequest } from '../utils/api'

const router = useRouter()
const message = ref('')
const isError = ref(false)

const form = ref({
  username: '',
  first_name: '',
  last_name: '',
  password: '',
  password_repeat: ''
})

const submitReg = async () => {
  message.value = ''
  isError.value = false

  if (form.value.password !== form.value.password_repeat) {
    isError.value = true
    message.value = 'Пароли не совпадают'
    return
  }

  try {
    const data = await advancedApiRequest('http://localhost:8000/admin/createuser', {
      method: 'POST',
      body: JSON.stringify(form.value)
    })
    
    isError.value = false
    message.value = 'Регистрация успешна! Теперь вы можете войти.'
    
    setTimeout(() => {
      router.push('/login')
    }, 1500)

  } catch (error) {
    isError.value = true
    message.value = 'Ошибка при регистрации. Возможно, логин уже занят.'
  }
}
</script>

<template>
    <div class="container">
        <h1>Регистрация</h1>
        <form id="register" @submit.prevent="submitReg">
            <div class="field">
                <input v-model="form.username" type="text" class="input-field" placeholder="Логин" required>
            </div>
            <div class="field">
                <input v-model="form.first_name" type="text" class="input-field" placeholder="Имя" required>
            </div>
            <div class="field">
                <input v-model="form.last_name" type="text" class="input-field" placeholder="Фамилия" required>
            </div>
            <div class="field">
                <input v-model="form.password" type="password" class="input-field" placeholder="Пароль" required>
            </div>
            <div class="field">
                <input v-model="form.password_repeat" type="password" class="input-field" placeholder="Подтвердить пароль" required>
            </div>
            
            <p v-if="message" :class="isError ? 'error-text' : 'success-text'">{{ message }}</p>
            
            <hr>
            <div class="button-field">
                <button type="submit" id="accept">Зарегистрироваться</button>
            </div>
            <div class="auth-link">
                <p>Уже есть аккаунт? <router-link to="/login">Войти</router-link></p>
            </div>
        </form>
    </div>
</template>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: #0b0e14;
    color: #222;
    margin: 120px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.container {
    display: flex;
    max-width: 800px;
    padding: 30px;
    align-items: center;
    flex-direction: column;
    border: solid 2px #777;
    border-radius: 30px;
    text-align: center;
    background-color: white;
}

h1 {
    color: #222;
    margin-bottom: 20px;
}

.field {
    display: block;
    margin-bottom: 20px;
    width: 400px;
    border: solid 2px #777;
    border-radius: 20px;
    height: 40px;
    text-align: left;
}

input {
    color: #222;
    font-size: 12px;
    border: none;
    margin: 13px 20px;
    outline: none;
    width: 90%;
}

hr {
    width: 90%;
    border: none;
    height: 1px;
    background-color: #777;
    margin: 30px auto;
}

.button-field {
    display: block;
    margin-bottom: 20px;
    width: 400px;
    border: solid 2px #222;
    background-color: #222;
    border-radius: 20px;
    height: 40px;
}

button {
    display: block;
    border: none;
    background-color: #222;
    color: #eee;
    margin: 10px auto;
    cursor: pointer;
    font-size: 16px;
    width: 100%;
}

p {
    font-size: 12px;
}

a {
    text-decoration: none;
    color: #4CAF50;
    font-weight: bold;
}

.error-text {
    color: red;
    margin-top: -10px;
    font-size: 14px;
}

.success-text {
    color: green;
    margin-top: -10px;
    font-size: 14px;
}
</style>
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const message = ref('')
const router = useRouter()

const submitLogin = async () => {
  message.value = ''
  try {
    const response = await fetch('http://localhost:8000/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({
        username: username.value,
        password: password.value
      })
    })

    if (!response.ok) {
      throw new Error('Неверный логин или пароль')
    }

    const data = await response.json()
    localStorage.setItem('token', data.access_token)
    
    // Определяем роль (если логин админский — кидаем в админку)
    if (username.value === 'admin') {
      localStorage.setItem('role', 'admin')
      router.push('/admin')
    } else {
      localStorage.setItem('role', 'user')
      router.push('/main')
    }

  } catch (error) {
    message.value = error.message
  }
}
</script>

<template>
    <div class="container">
        <h1>Вход</h1>
        <form id="register" @submit.prevent="submitLogin">
            <div class="field">
                <input v-model="username" type="text" class="input-field" placeholder="Логин" required>
            </div>
            <div class="field">
                <input v-model="password" type="password" class="input-field" placeholder="Пароль" required>
            </div>
            
            <p v-if="message" class="error-text">{{ message }}</p>
            
            <hr>
            <div class="button-field">
                <button type="submit" id="accept">Войти</button>
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
</style>
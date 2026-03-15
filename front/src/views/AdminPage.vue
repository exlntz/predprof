<script setup>
import { ref } from 'vue'
import { advancedApiRequest } from '../utils/api'

const message = ref('')
const isError = ref(false)

const newUser = ref({
  username: '',
  first_name: '',
  last_name: '',
  password: '',
  password_repeat: '',
  is_admin: false
})

const createUser = async () => {
  message.value = ''
  isError.value = false
  
  if (newUser.value.password !== newUser.value.password_repeat) {
    isError.value = true
    message.value = 'Пароли не совпадают'
    return
  }

  try {
    const response = await advancedApiRequest('http://localhost:8000/admin/createuser', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(newUser.value)
    })
    
    message.value = 'Пользователь успешно добавлен!'
    newUser.value = {
      username: '',
      first_name: '',
      last_name: '',
      password: '',
      password_repeat: '',
      is_admin: false
    }
  } catch (error) {
    isError.value = true
    message.value = 'Ошибка при создании пользователя. Возможно, логин уже занят.'
  }
}
</script>

<template>
  <div class="admin-container">
    <h2>Панель администратора</h2>

    <div class="form-container">
      <h3>Добавить пользователя</h3>
      <form @submit.prevent="createUser" class="user-form">
        <input v-model="newUser.username" type="text" placeholder="Логин" required />
        <input v-model="newUser.first_name" type="text" placeholder="Имя" required />
        <input v-model="newUser.last_name" type="text" placeholder="Фамилия" required />
        <input v-model="newUser.password" type="password" placeholder="Пароль" required />
        <input v-model="newUser.password_repeat" type="password" placeholder="Повторите пароль" required />
        
        <label class="checkbox-label">
          <input v-model="newUser.is_admin" type="checkbox" />
          Назначить администратором
        </label>

        <button type="submit">Создать</button>
      </form>
      <p v-if="message" :class="{ 'error-text': isError, 'success-text': !isError }">
        {{ message }}
      </p>
    </div>
  </div>
</template>

<style scoped>
.admin-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  font-family: sans-serif;
}

.form-container {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.user-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.user-form input[type="text"],
.user-form input[type="password"] {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 15px;
  color: #333;
  cursor: pointer;
  user-select: none;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.user-form button {
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

.user-form button:hover {
  background-color: #45a049;
}

.error-text {
  color: red;
  margin-top: 10px;
}

.success-text {
  color: green;
  margin-top: 10px;
}
</style>
<template>
    <div class="container">
      <h2>Создание нового пользователя</h2>
      
      <form @submit.prevent="addUser">
        <div class="input-group">
          <label>Имя:</label>
          <input v-model="newUser.first_name" type="text" required placeholder="Введите имя" />
        </div>
        
        <div class="input-group">
          <label>Фамилия:</label>
          <input v-model="newUser.last_name" type="text" required placeholder="Введите фамилию" />
        </div>
        
        <button type="submit">Добавить</button>
      </form>
  
      <hr />
  
      <h2>Список пользователей</h2>
      <ul v-if="users.length > 0">
        <li v-for="(user, index) in users" :key="index">
          {{ user.first_name }} {{ user.last_name }}
        </li>
      </ul>
      <p v-else>Список пока пуст.</p>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  
  const users = ref([])
  const newUser = ref({ first_name: '', last_name: '' })
  
  const fetchUsers = async () => {
    const response = await fetch('http://localhost:8000/api/users')
    if (response.ok) {
      users.value = await response.json()
    }
  }
  
  const addUser = async () => {
    const response = await fetch('http://localhost:8000/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newUser.value)
    })
  
    if (response.ok) {
      newUser.value.first_name = ''
      newUser.value.last_name = ''
      await fetchUsers()
    }
  }
  
  onMounted(() => {
    fetchUsers()
  })
  </script>
  
  <style scoped>
  .container {
    max-width: 500px;
    margin: 0 auto;
    font-family: sans-serif;
  }
  .input-group {
    margin-bottom: 10px;
  }
  label {
    display: inline-block;
    width: 80px;
  }
  button {
    margin-top: 10px;
    padding: 5px 15px;
  }
  </style>
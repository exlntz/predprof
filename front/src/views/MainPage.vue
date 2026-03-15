<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { advancedApiRequest } from '../utils/api'

const user = ref(null)
const errorMsg = ref('')
const activeTab = ref('profile')
const router = useRouter()

const fetchProfile = async () => {
  try {
    const data = await advancedApiRequest('http://localhost:8000/auth/me', {
      method: 'GET'
    })
    user.value = data
  } catch (error) {
    errorMsg.value = 'Ошибка при загрузке профиля'
  }
}

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('role')
  router.push('/login')
}

onMounted(() => {
  fetchProfile()
})
</script>

<template>
  <div class="main-container">
    <header class="header">
      <h2>Панель исследователя</h2>
      <button @click="logout" class="logout-btn">Выйти</button>
    </header>
    <hr>

    <div class="tabs">
      <button 
        :class="['tab-btn', { active: activeTab === 'profile' }]" 
        @click="activeTab = 'profile'"
      >
        Профиль
      </button>
      <button 
        :class="['tab-btn', { active: activeTab === 'analytics' }]" 
        @click="activeTab = 'analytics'"
      >
        Аналитика
      </button>
    </div>

    <div class="content-area">
      <div v-if="activeTab === 'profile'" class="tab-content">
        <div v-if="user" class="profile-card">
          <h3>Мой профиль</h3>
          <div class="profile-info">
            <p><strong>Логин:</strong> {{ user.username }}</p>
            <p><strong>Имя:</strong> {{ user.first_name }}</p>
            <p><strong>Фамилия:</strong> {{ user.last_name }}</p>
          </div>
        </div>
        <div v-else-if="errorMsg" class="error-text">{{ errorMsg }}</div>
        <div v-else class="loading-text">Загрузка...</div>
      </div>

      <div v-if="activeTab === 'analytics'" class="tab-content">
        <div class="analytics-container">
          <h3>Визуализация данных</h3>
          <div class="charts-grid">
            <div class="chart-placeholder">
              <p>График точности обучения</p>
              </div>
            <div class="chart-placeholder">
              <p>Распределение классов</p>
            </div>
            <div class="chart-placeholder">
              <p>Точность по записям</p>
            </div>
            <div class="chart-placeholder">
              <p>Топ-5 цивилизаций</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

.main-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 30px;
  font-family: sans-serif;
  background-color: white;
  border-radius: 30px;
  text-align: center;
}

.header {
  width: 600px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

h2 {
  color: #222;
  border-right: solid 1px #222;
  padding-right: 20px;
}

.logout-btn {
  padding: 8px 16px;
  background-color: #e74c3c;
  color: white;
  width: 100px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 100px;
}

.logout-btn:hover {
  background-color: #c0392b;
}

hr {
  width: 100%;
  height: 2px;
  border: none;
  background-color: #222;
}

.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
}

.tab-btn {
  padding: 10px 20px;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 16px;
  color: #666;
}

.tab-btn.active {
  color: #4CAF50;
  border-bottom: 3px solid #4CAF50;
  font-weight: bold;
}

.profile-card, .analytics-container {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 20px;
}

.chart-placeholder {
  background: #e9e9e9;
  height: 250px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px dashed #999;
  border-radius: 20px;
}

.profile-info p {
  margin: 15px 0;
  font-size: 17px;
}
</style>
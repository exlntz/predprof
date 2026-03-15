<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const tab = ref('profile')
const router = useRouter()

const logout = () => {
  localStorage.clear()
  router.push('/login')
}
</script>

<template>
    <div class="page-container">
      <header class="tab-nav">
        <button :class="{ active: tab === 'profile' }" @click="tab = 'profile'">Профиль</button>
        <button :class="{ active: tab === 'analytics' }" @click="tab = 'analytics'">Анализ Сигналов</button>
        <button @click="logout" class="exit-btn">Выход</button>
      </header>
  
      <main class="content">
        <section v-if="tab === 'profile'">
          <h1>Карточка сотрудника №001</h1>
          <div class="user-card">




          </div>
        </section>
  
        <section v-if="tab === 'analytics'">
          <h1>Аналитика ИИ моделей</h1>
          <div class="charts-grid">
            <canvas id="accuracyChart"></canvas>
            <canvas id="distributionChart"></canvas>
          </div>
        </section>
      </main>
    </div>
  </template>
  

  
  <style scoped>
  .page-container { display: flex; flex-direction: column; height: 100vh; }
  .tab-nav { display: flex; background: #1a1f26; padding: 10px; gap: 10px; }
  .active { border-bottom: 2px solid #42b883; color: #42b883; }
  .exit-btn { margin-left: auto; color: #ff5555; border: none; background: none; cursor: pointer; }
  </style>
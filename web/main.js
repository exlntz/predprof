import { createApp } from 'vue'
import app from './app.vue'
import router from './utils/router' // Импорт твоего роутера

const app = createApp(app)
app.use(router) // БЕЗ ЭТОГО БУДЕТ БЕЛЫЙ ЭКРАН
app.mount('#app')
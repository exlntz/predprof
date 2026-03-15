import { createApp } from 'vue'
import App from './App.vue'
import router from './utils/router' // Импорт твоего роутера

const app = createApp(App)
app.use(router) // БЕЗ ЭТОГО БУДЕТ БЕЛЫЙ ЭКРАН
app.mount('#app')
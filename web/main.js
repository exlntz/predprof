import { createApp } from 'vue'
import App from './app.vue'
import router from './src/styles/utils/router' // Импорт твоего роутера

const app = createApp(App)
app.use(router) // БЕЗ ЭТОГО БУДЕТ БЕЛЫЙ ЭКРАН
app.mount('#app')
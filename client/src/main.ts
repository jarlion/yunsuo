import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus, { ElMessage } from 'element-plus'
import 'element-plus/dist/index.css'
import { TaskManager } from '@/models/Task';
import { createSingleton } from '@/utils/singleton';
import { init } from './conn/Connection';

const taskManager = new TaskManager();
createSingleton(taskManager, 'taskManager').init();

const app = createApp(App)
app.use(ElementPlus)
app.mount('#app')

init(ElMessage);

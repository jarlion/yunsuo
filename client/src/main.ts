import ElementPlus, { ElMessage } from 'element-plus';
import { createApp } from 'vue';

import ArrayInput from '@/components/input/ArrayInput.vue';
import BooleanInput from '@/components/input/BoolenInput.vue';
import CodeInput from '@/components/input/CodeInput.vue';
import TextInput from '@/components/input/TextInput.vue';
import { TaskManager } from '@/models/Task';
import { createSingleton } from '@/utils/singleton';
import 'element-plus/dist/index.css';
import App from './App.vue';
import { init } from './conn/Connection';
import './global.css';

const taskManager = new TaskManager();
createSingleton(taskManager, 'taskManager').init();

const app = createApp(App)
app.use(ElementPlus)
app.component('TextInput', TextInput)
app.component('CodeInput', CodeInput)
app.component('ArrayInput', ArrayInput)
app.component('BooleanInput', BooleanInput)
app.mount('#app')

init(ElMessage);

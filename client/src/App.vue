<script setup lang="ts">
import PipelineEditor from './pages/PipelineEditor.vue'
import { ElMessage } from 'element-plus'
import 'element-plus/dist/index.css'
import PipelineEdit from '@/PipelineEdit.vue'
import TaskPane from '@/components/panes/TaskPane.vue'


</script>

<template>
  <div class="app-container">
    <!-- <PipelineEditor />
      -->
    <PipelineEdit />
    <TaskPane />
  </div>
</template>

<style scoped>
.app-container {
  height: 100vh;
  width: 100%;
}
</style>

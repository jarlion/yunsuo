<template>
  <div class="pipeline-editor-container">
    <!-- 左右布局容器 -->
    <el-container style="height: 100vh;">
      <!-- 左侧流水线管理面板 -->
      <el-aside width="300px" class="left-panel">
        <div class="panel-header">
          <h2>流水线管理</h2>
          <el-button type="primary" size="small" @click="addPipeline">新建流水线</el-button>
        </div>
        
        <el-list v-if="pipelines.length > 0" border>
          <el-list-item v-for="pipeline in pipelines" :key="pipeline.id" class="pipeline-item">
            <div class="pipeline-info">
              <h3>{{ pipeline.name }}</h3>
              <p>{{ pipeline.description }}</p>
            </div>
            <div class="pipeline-actions">
              <el-button type="primary" size="small" @click="editPipeline(pipeline)">编辑</el-button>
              <el-button type="danger" size="small" @click="deletePipeline(pipeline.id)">删除</el-button>
            </div>
          </el-list-item>
        </el-list>
        
        <div v-else class="empty-state">
          <p>暂无流水线，请点击新建按钮创建</p>
        </div>
      </el-aside>

      <!-- 右侧命令面板 -->
      <el-main class="right-panel">
        <div class="command-panel">
          <h2>命令面板</h2>
          
          <!-- 查询表单 -->
          <el-form :inline="true" class="search-form">
            <el-form-item>
              <el-input
                v-model="searchQuery"
                placeholder="输入code或name"
                style="width: 300px;"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="searchCommands">查询</el-button>
            </el-form-item>
          </el-form>

          <!-- 结果表格 -->
          <el-table
            v-loading="loading"
            :data="commandList"
            style="width: 100%; margin-top: 20px;"
          >
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="code" label="Code" width="180" />
            <el-table-column prop="name" label="Name" width="180" />
            <el-table-column prop="description" label="Description" />
            <el-table-column prop="createdAt" label="Created At" width="180" />
          </el-table>

          <!-- 分页组件 -->
          <div class="pagination-container">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :page-sizes="[10, 20, 50, 100]"
              layout="total, sizes, prev, pager, next, jumper"
              :total="total"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </div>
        </div>
      </el-main>
    </el-container>

    <!-- 新建/编辑流水线对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
    >
      <el-form ref="pipelineForm" :model="formData" label-width="100px">
        <el-form-item label="流水线名称" prop="name" :rules="[{ required: true, message: '请输入流水线名称', trigger: 'blur' }]">
          <el-input v-model="formData.name" placeholder="请输入流水线名称" />
        </el-form-item>
        <el-form-item label="流水线描述" prop="description">
          <el-input v-model="formData.description" type="textarea" placeholder="请输入流水线描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="savePipeline">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import axios from 'axios';
import { ElAside, ElButton, ElContainer, ElDialog, ElForm, ElInput, ElMessage, ElPagination, ElTable, ElTableColumn } from 'element-plus';
import { onMounted, reactive, ref } from 'vue';

// 流水线数据
const pipelines = ref<any[]>([]);
const dialogVisible = ref(false);
const dialogTitle = ref('新建流水线');
const formData = reactive({ id: '', name: '', description: '' });

// 命令面板数据
const searchQuery = ref('');
const commandList = ref<any[]>([]);
const loading = ref(false);
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);

// 页面加载时获取流水线列表
onMounted(() => {
  fetchPipelines();
});

// 获取流水线列表
const fetchPipelines = async () => {
  try {
    // 这里应该调用实际的API
    // 模拟数据
    pipelines.value = [
      { id: '1', name: '测试流水线1', description: '这是第一个测试流水线' },
      { id: '2', name: '测试流水线2', description: '这是第二个测试流水线' }
    ];
  } catch (error) {
    ElMessage.error('获取流水线列表失败');
    console.error('Failed to fetch pipelines:', error);
  }
};

// 新建流水线
const addPipeline = () => {
  dialogTitle.value = '新建流水线';
  Object.keys(formData).forEach(key => {
    formData[key as keyof typeof formData] = '';
  });
  dialogVisible.value = true;
};

// 编辑流水线
const editPipeline = (pipeline: any) => {
  dialogTitle.value = '编辑流水线';
  Object.assign(formData, pipeline);
  dialogVisible.value = true;
};

// 保存流水线
const savePipeline = async () => {
  try {
    // 这里应该调用实际的API
    if (formData.id) {
      // 更新流水线
      const index = pipelines.value.findIndex(p => p.id === formData.id);
      if (index !== -1) {
        pipelines.value[index] = { ...formData };
      }
      ElMessage.success('流水线更新成功');
    } else {
      // 新建流水线
      const newPipeline = { ...formData, id: Date.now().toString() };
      pipelines.value.push(newPipeline);
      ElMessage.success('流水线创建成功');
    }
    dialogVisible.value = false;
  } catch (error) {
    ElMessage.error('保存流水线失败');
    console.error('Failed to save pipeline:', error);
  }
};

// 删除流水线
const deletePipeline = async (id: string) => {
  try {
    // 这里应该调用实际的API
    pipelines.value = pipelines.value.filter(p => p.id !== id);
    ElMessage.success('流水线删除成功');
  } catch (error) {
    ElMessage.error('删除流水线失败');
    console.error('Failed to delete pipeline:', error);
  }
};

// 搜索命令
const searchCommands = async () => {
  try {
    loading.value = true;
    // 调用cmd/list API
    const response = await axios.get('/api/cmd/list', {
      params: {
        query: searchQuery.value,
        page: currentPage.value,
        pageSize: pageSize.value
      }
    });
    commandList.value = response.data.items;
    total.value = response.data.total;
  } catch (error) {
    ElMessage.error('查询命令失败');
    console.error('Failed to search commands:', error);
  } finally {
    loading.value = false;
  }
};

// 分页处理
const handleSizeChange = (size: number) => {
  pageSize.value = size;
  searchCommands();
};

const handleCurrentChange = (current: number) => {
  currentPage.value = current;
  searchCommands();
};
</script>

<style scoped>
.pipeline-editor-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.left-panel {
  background-color: #f5f7fa;
  border-right: 1px solid #e6e6e6;
  overflow-y: auto;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #e6e6e6;
}

.pipeline-item {
  padding: 12px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pipeline-info {
  flex: 1;
}

.pipeline-actions {
  display: flex;
  gap: 8px;
}

.empty-state {
  padding: 24px;
  text-align: center;
  color: #909399;
}

.right-panel {
  padding: 20px;
  overflow-y: auto;
}

.command-panel {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.search-form {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
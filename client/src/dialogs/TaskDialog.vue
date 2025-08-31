<template>
  <el-dialog
    :title="title"
    v-model="visible"
    width="700"
    :before-close="onClose"
  >
    <el-space fill>
      <el-alert type="info" title="任务参数" :closable="false" />
      <el-form label-width="100px" :rules="rules" :model="modelJson">
        <el-form-item label="ctx">
          <el-input v-model="ctx" />
        </el-form-item>
        <el-form-item label="code">
          <TaskSelect v-model="model.code" />
        </el-form-item>
        <el-form-item label="on">
          <el-switch v-model="model.on" />
        </el-form-item>
        <el-form-item
          v-for="prop in task?.params || []"
          :key="prop.name"
          :label="prop.name"
          :prop="prop.name"
        >
          <!-- <el-input v-model="modelJson[prop]" /> -->
          <component
            :is="getComponent(task, prop.name)"
            v-model="model.params[prop.name]"
            :placeholder="getTaskParamDef(task, prop.name)?.placeholder"
          />
        </el-form-item>
      </el-form>
      <el-alert type="info" title="调试结果" :closable="false" />
      <el-input type="textarea" v-model="result" />
    </el-space>
    <template #footer>
      <el-button-group class="ys-right-space">
        <el-button :icon="Download" @click="onSaveTemp">暂存</el-button>
        <el-button :icon="Upload" @click="onLoadTemp">加载暂存</el-button>
        <el-button type="primary" :icon="DArrowRight" @click="onTest">
          {{ `调试` }}
        </el-button>
      </el-button-group>
      <el-button :icon="CloseBold" @click="onClose">Cancel</el-button>
      <el-button :icon="Select" type="primary" @click="onOk">
        Submit
      </el-button>
    </template>
  </el-dialog>
</template>
<script lang="ts" setup>
import {
  DArrowRight,
  Download,
  Select,
  Upload,
  CloseBold,
} from "@element-plus/icons-vue";
import { ElInput, ElMessage } from "element-plus";
import { computed, ref, watch, type ComputedRef, type Ref } from "vue";

import {
  type ITask,
  type ITaskConfig,
  type TaskManager,
  getComponent,
  getTaskParamDef,
} from "@/models/Task";
import { test } from "@/protocols/task/test";
import { getSingleton } from "@/utils/singleton";
import TaskSelect from "@/components/select/TaskSelect.vue";

const emit = defineEmits(["update:modelValue"]);

const title = ref("");

const visible = ref(false);

const props = defineProps({
  ctx: {
    type: Object,
    default: () => ({}),
  },
});

const model: Ref<ITaskConfig> = ref({
  id: "",
  pipelineId: "",
  code: "",
  on: true,
  params: {},
});

const modelJson = ref({});
const ctx = ref(JSON.stringify(props.ctx));

const task: ComputedRef<ITask> = computed(
  () =>
    getSingleton<TaskManager>("taskManager")?.getTask(model.value.code) || {
      params: [],
      id: "",
      code: "",
      name: "",
    }
);

const rules = computed(() => {
  const kvs =
    task.value?.params.map((p) => [
      p.name,
      { required: p.required, trigger: "blur" },
    ]) || [];
  return Object.fromEntries(kvs);
});

const result = ref("");

function initModel(model: Record<string, any>): Record<string, string | any[]> {
  return Object.fromEntries(
    Object.entries(model).map(([k, v]) => [
      k,
      v
        ? typeof v === "string" && v.match(/^[\{\[]/)
          ? JSON.stringify(v)
          : v
        : "",
    ])
  );
}

function modelToObject(model: Record<string, string>): Record<string, any> {
  return Object.fromEntries(
    Object.entries(model).map(([k, v]) => {
      let value = v;
      try {
        value = JSON.parse(v);
      } catch (err) {
        // 忽略解析错误
      }
      return [k, value];
    })
  );
}

watch(
  () => props.ctx,
  (val) => {
    ctx.value = JSON.stringify(val);
  }
);

watch(
  () => props.modelValue,
  (val) => {
    modelJson.value = initModel(val);
  }
);

async function onTest() {
  try {
    const res = await test({
      code: props.code,
      params: modelToObject(modelJson.value),
      ctx: JSON.parse(ctx.value),
    });
    result.value = JSON.stringify(res);
  } catch (err) {
    result.value = (err as Error).message;
  }
}

function onSaveTemp() {
  try {
    localStorage.setItem(
      props.code,
      JSON.stringify({ params: modelToObject(modelJson.value), ctx: ctx.value })
    );
    ElMessage.success("暂存成功");
  } catch (err) {
    ElMessage.error((err as Error).message);
  }
}

function onLoadTemp() {
  try {
    const res = localStorage.getItem(props.code);
    if (res) {
      const data = JSON.parse(res);
      modelJson.value = initModel(data.params);
      ctx.value = data.ctx;
    }
    ElMessage.success("加载暂存成功");
  } catch (err) {
    ElMessage.error((err as Error).message);
  }
}

function onClose() {
  visible.value = false;
}
function onOk() {
  emit("update:modelValue", modelToObject(modelJson.value));
}

function show(tc: ITaskConfig) {
  title.value = `编辑任务 ${tc.id}` || `新建任务`;
  modelJson.value = initModel(tc);
  visible.value = true;
}

defineExpose({
  show,
});
</script>
<style scoped>
.ys-right-space {
  margin-right: 30px;
}
</style>

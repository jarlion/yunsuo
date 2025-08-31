<template>
  <el-dialog
    :title="title"
    v-model="visible"
    width="700"
    :before-close="onClose"
    :close-on-click-modal="false"
  >
    <el-space fill>
      <el-alert type="info" title="任务参数" :closable="false" />
      <el-form
        ref="taskFormRef"
        label-width="100px"
        :rules="rules"
        :model="model.params"
      >
        <el-form-item label="ctx">
          <el-input v-model="ctx" />
        </el-form-item>
        <el-form-item label="code">
          <TaskSelect v-model="model.code" @change="onTaskCodeChange" />
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
      <el-button
        :icon="CloseBold"
        @click="onClose"
        :loading="loading"
      />
      <el-button :icon="Select" type="primary" @click="onOk" :loading="loading" />
    </template>
  </el-dialog>
</template>
<script lang="ts" setup>
import {
  CloseBold,
  DArrowRight,
  Download,
  Select,
  Upload,
} from "@element-plus/icons-vue";
import { ElForm, ElInput, ElMessage } from "element-plus";
import {
  computed,
  ref,
  shallowRef,
  unref,
  watch,
  type Ref,
  type ShallowRef,
} from "vue";

import TaskSelect from "@/components/select/TaskSelect.vue";
import {
  clone,
  getComponent,
  getTaskParamDef,
  initBy,
  type ITask,
  type ITaskConfig,
  type TaskManager,
} from "@/models/Task";
import { toTaskParams } from "@/protocols/base/ITaskParams";
import { test } from "@/protocols/task/test";
import { update } from "@/protocols/task/update";
import { getSingleton } from "@/utils/singleton";

const emit = defineEmits(["ok"]);

const title = ref("");

const visible = ref(false);

const taskFormRef = ref<typeof ElForm>();

const props = defineProps({
  ctx: {
    type: Object,
    default: () => ({}),
  },
});

const loading = ref(false);

const model: Ref<ITaskConfig> = ref({
  id: "",
  pipelineId: "",
  code: "",
  on: true,
  params: {},
});

const ctx = ref(JSON.stringify(props.ctx));

const task: ShallowRef<ITask> = shallowRef({
  params: [],
  id: "",
  code: "",
  name: "",
});

function onTaskCodeChange(code: string) {
  const targetTask = getSingleton<TaskManager>("taskManager")?.getTask(code);
  if (targetTask) {
    task.value = targetTask;
    model.value.params = initBy(task.value.params);
  }
}

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

async function onTest() {
  try {
    const res = await test({
      code: model.value.code,
      params: modelToObject(model.value.params),
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
      model.value.id,
      JSON.stringify({
        params: model.value.params,
        ctx: ctx.value,
      })
    );
    ElMessage.success("暂存成功");
  } catch (err) {
    ElMessage.error((err as Error).message);
  }
}

function onLoadTemp() {
  try {
    const res = localStorage.getItem(model.value.id);
    if (res) {
      const data = JSON.parse(res);
      model.value.params = data.params;
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
async function onOk() {
  try {
    await unref(taskFormRef)?.validate();
  } catch (err) {
    // 校验失败
    return;
  }
  try {
    loading.value = true;
    const params = toTaskParams(unref(model));
    const task = await update(params);
    emit("ok", task);
    onClose();
  } catch (err) {
    ElMessage.error((err as Error).message);
  } finally {
    loading.value = false;
  }
}

function show(tc: ITaskConfig) {
  title.value = `编辑任务 ${tc.id}` || `新建任务`;
  model.value = clone(tc);
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

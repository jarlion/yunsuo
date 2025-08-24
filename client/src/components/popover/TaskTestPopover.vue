<template>
  <el-popover placement="right" :width="400" trigger="click">
    <template #reference>
      <slot>
        <el-button :icon="Promotion" type="primary" link> </el-button>
      </slot>
    </template>
    <div>{{ `${code} : ${task?.name}` }}</div>
    <el-form label-width="100px">
      <el-form-item label="params">
        <el-input v-model="params" />
      </el-form-item>
      <el-form-item label="ctx">
        <el-input v-model="ctx" />
      </el-form-item>
      <el-form-item label="result">
        {{ result }}
      </el-form-item>
    </el-form>
    <el-button :icon="Download" @click="onSaveTemp">Quick Save</el-button>
    <el-button :icon="Upload" @click="onLoadTemp">Quick Load</el-button>
    <el-button type="primary" :icon="Promotion" @click="onTest">Test</el-button>
  </el-popover>
</template>

<script lang="ts" setup>
import { initRecord, type TaskManager } from "@/models/Task";
import { test } from "@/protocols/tasks/test";
import { getSingleton } from "@/utils/singleton";
import { Download, Promotion, Upload } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import { computed, ref, watch } from "vue";

const model = defineModel({
  type: Object,
});

const props = defineProps({
  rules: {
    type: Array,
    default: () => [],
  },
  code: {
    type: String,
    default: "",
  },
});

const task = computed(() =>
  getSingleton<TaskManager>("taskManager")?.getTask(props.code)
);

const params = ref(
  task.value?.params ? JSON.stringify(initRecord(task.value?.params)) : ""
);
const ctx = ref(
  task.value?.ctx ? JSON.stringify(initRecord(task.value?.ctx)) : ""
);

const result = ref("");

watch(
  () => task.value,
  (t) => {
    params.value = t?.params ? JSON.stringify(initRecord(t.params)) : "";
    ctx.value = t?.ctx ? JSON.stringify(initRecord(t.ctx)) : "";
  }
);

async function onTest() {
  try {
    const res = await test({
      code: props.code,
      params: JSON.parse(params.value),
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
      JSON.stringify({ params: params.value, ctx: ctx.value })
    );
  } catch (err) {
    ElMessage.error((err as Error).message);
  }
}

function onLoadTemp() {
  try {
    const res = localStorage.getItem(props.code);
    if (res) {
      const data = JSON.parse(res);
      params.value = data.params;
      ctx.value = data.ctx;
    }
  } catch (err) {
    ElMessage.error((err as Error).message);
  }
}
</script>

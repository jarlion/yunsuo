<template>
  <el-popover placement="right" :width="400" trigger="click">
    <template #reference>
      <slot>
        <el-button :icon="Operation" type="primary" link> </el-button>
      </slot>
    </template>
    <el-space fill>
      <el-alert type="info" title="任务参数" :closable="false" />
      <el-form label-width="100px" :rules="rules" :model="modelJson">
        <el-form-item label="ctx">
          <el-input v-model="ctx" />
        </el-form-item>
        <el-form-item
          v-for="prop in Object.keys(modelJson)"
          :key="prop"
          :label="prop"
          :prop="prop"
        >
          <el-input v-model="modelJson[prop]" />
        </el-form-item>
      </el-form>
      <el-alert type="info" title="调试结果" :closable="false" />
      <el-input type="textarea" v-model="result" />
      <div class="ys-align-right">
        <el-button-group>
          <el-button :icon="Download" @click="onSaveTemp">暂存</el-button>
          <el-button :icon="Upload" @click="onLoadTemp">加载暂存</el-button>
          <el-button type="primary" :icon="CaretRight" @click="onTest">{{
            `调试 ${task?.name} ${code}`
          }}</el-button>
        </el-button-group>
      </div>
    </el-space>
  </el-popover>
</template>

<script lang="ts" setup>
import { type TaskManager } from "@/models/Task";
import { test } from "@/protocols/tasks/test";
import { getSingleton } from "@/utils/singleton";
import {
  CaretRight,
  Download,
  Operation,
  Upload,
} from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import { computed, ref, watch } from "vue";

const emit = defineEmits(["update:modelValue"]);

const props = defineProps({
  code: {
    type: String,
    default: "",
  },
  ctx: {
    type: Object,
    default: () => ({}),
  },
  modelValue: {
    type: Object,
    default: () => {},
  },
});

const modelJson = ref(initModel(props.modelValue));
const ctx = ref(JSON.stringify(props.ctx));

const task = computed(() =>
  getSingleton<TaskManager>("taskManager")?.getTask(props.code)
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

function initModel(model: Record<string, any>): Record<string, string> {
  return Object.fromEntries(
    Object.entries(model).map(([k, v]) => [k, v ? JSON.stringify(v) : ""])
  );
}

function modelToObject(model: Record<string, string>): Record<string, any> {
  return Object.fromEntries(
    Object.entries(model).map(([k, v]) => [k, v ? JSON.parse(v) : ""])
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
</script>

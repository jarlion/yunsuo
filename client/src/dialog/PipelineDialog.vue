<template>
  <el-dialog
    title="Pipeline Dialog"
    v-model="visible"
    width="50%"
    :before-close="onClose"
  >
    <el-form :model="model" :rules="rules" ref="formRef" label-width="120px">
      <el-form-item label="Code" prop="code">
        <el-input v-model="model.code" :disabled="!isCodeEditable" />
      </el-form-item>
      <el-form-item label="Desc" prop="desc">
        <el-input v-model="model.desc" />
      </el-form-item>
      <el-form-item label="Name" prop="name">
        <el-input v-model="model.name" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button type="primary" @click="onOk">Submit</el-button>
      <el-button @click="onClose">Cancel</el-button>
    </template>
  </el-dialog>
</template>
<script setup lang="ts">
import type { IPipeline } from "@/model/Pipeline";
import {
    ElButton,
    ElDialog,
    ElForm,
    ElFormItem,
    ElInput
} from "element-plus";

import { ref } from "vue";

const emit = defineEmits(["ok"]);

const visible = ref(false);
const model = ref<IPipeline>(initModel());
const rules = ref({
  name: [{ required: true, message: "请输入名称", trigger: "blur" }],
  desc: [{ required: true, message: "请输入描述", trigger: "blur" }],
});

const isCodeEditable = ref(false);

function show(pipeline?: IPipeline) {
  if (pipeline) {
    model.value = pipeline;
    isCodeEditable.value = pipeline.code?.length === 0;
  }

  visible.value = true;
}

function onClose() {
  visible.value = false;
  model.value = initModel();
}

function onOk() {
  emit("ok", { ...model.value });
  onClose();
}

function initModel(): IPipeline {
  return {
    name: "",
    code: "",
    desc: "",
    stars: 0,
    tasks: [],
  };
}

defineExpose({ show });
</script>

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
      <el-form-item label="Name" prop="name">
        <el-input v-model="model.name" />
      </el-form-item>
      <el-form-item label="Desc" prop="desc">
        <el-input v-model="model.desc" />
      </el-form-item>
      <el-form-item label="Context" prop="ctx">
        <el-input v-model="model.ctx" />
      </el-form-item>
    </el-form>
    <TaskConfigListEditPane v-model="model.tasks" :width="500" :height="300"/>
    <template #footer>
      <el-button @click="onClose">Cancel</el-button>
      <el-button type="primary" @click="onOk">Submit</el-button>
    </template>
  </el-dialog>
</template>
<script setup lang="ts">
import { clone, create, type IPipeline } from "@/models/Pipeline";
import {
    ElButton,
    ElDialog,
    ElForm,
    ElFormItem,
    ElInput
} from "element-plus";

import { ref } from "vue";
import TaskConfigListEditPane from "@/components/panes/TaskConfigListEditPane.vue";

const emit = defineEmits(["ok"]);

const visible = ref(false);
const model = ref<IPipeline>(create());
const rules = ref({
  name: [{ required: true, message: "请输入名称", trigger: "blur" }],
  desc: [{ required: true, message: "请输入描述", trigger: "blur" }],
});

const isCodeEditable = ref(false);

function show(pipeline?: IPipeline) {
  if (pipeline) {
    model.value = clone(pipeline);
    isCodeEditable.value = pipeline.code?.length === 0;
  }

  visible.value = true;
}

function onClose() {
  visible.value = false;
  model.value = create();
}

function onOk() {
  emit("ok", { ...model.value });
  onClose();
}


defineExpose({ show });
</script>

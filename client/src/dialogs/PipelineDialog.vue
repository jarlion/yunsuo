<template>
  <el-dialog
    :title="title"
    v-model="visible"
    width="700"
    :before-close="onClose"
  >
    <el-form :model="model" :rules="rules" ref="formRef" label-width="120px">
      <el-form-item label="Name" prop="name">
        <el-input v-model="model.name" />
      </el-form-item>
      <el-form-item label="Desc" prop="desc">
        <el-input v-model="model.desc" />
      </el-form-item>
      <el-form-item label="Context" prop="ctx">
        <ObjectInput v-model="model.ctx" />
      </el-form-item>
    </el-form>
    <TaskConfigListEditPane
      v-model="model.tasks"
      :pipelineId="model.id"
      :ctx="model.ctx"
      :width="500"
      :height="300"
    />
    <template #footer>
      <el-button :icon="CloseBold" @click="onClose">Cancel</el-button>
      <el-button :icon="Select" type="primary" @click="onOk">Submit</el-button>
    </template>
  </el-dialog>
</template>
<script setup lang="ts">
import { CloseBold, Select } from "@element-plus/icons-vue";
import { ElButton, ElDialog, ElForm, ElFormItem, ElInput } from "element-plus";
import { ref, unref } from "vue";

import TaskConfigListEditPane from "@/components/panes/TaskConfigListEditPane.vue";
import { clone, create, type IPipeline } from "@/models/Pipeline";
import ObjectInput from "@/components/input/ObjectInput.vue";

const emit = defineEmits(["ok"]);

const visible = ref(false);
const title = ref("");
const model = ref<IPipeline>(create());
const rules = ref({
  name: [{ required: true, message: "请输入名称", trigger: "blur" }],
  ctx: [{ required: true, message: "请输入上下文", trigger: "blur" }],
});

const isCodeEditable = ref(false);

function show(pipeline?: IPipeline) {
  if (pipeline) {
    model.value = clone(pipeline);
    isCodeEditable.value = pipeline.code?.length === 0;
  }
  title.value = model.value.id ? `编辑 ${model.value.id.toUpperCase()}` : "新增流水线";
  visible.value = true;
}

function onClose() {
  visible.value = false;
  model.value = create();
}

function onOk() {
  emit("ok", unref(model.value));
  onClose();
}

defineExpose({ show });
</script>

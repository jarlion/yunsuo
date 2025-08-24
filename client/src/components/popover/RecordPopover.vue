<template>
  <el-popover placement="right" :width="400" trigger="click">
    <template #reference>
      <slot>
        <el-button :icon="Edit" type="primary" link>
            {{ toContent(model) }} 
            <!-- <el-icon><Edit /></el-icon> -->
        </el-button>
      </slot>
    </template>
    <el-form :model="model" :rules="rules" ref="formRef">
      <el-form-item v-for="key in Object.keys(model)" :label="key">
        <el-input v-model="model[key]" />
      </el-form-item>
    </el-form>
  </el-popover>
</template>

<script lang="ts" setup>
import { Edit } from "@element-plus/icons-vue";

const model = defineModel({
  type: Object,
});

const props = defineProps({
  rules: {
    type: Array,
    default: () => [],
  },
  toContent: {
    type: Function,
    default: (model: Record<string, any>) => Object.keys(model).map((key) => `${key}: ${model[key]}`).join('\n'),
  },
});
</script>

<
<template>
  <el-input v-model="model" v-bind="$attrs" @change="onChange" />
</template>
<script lang="ts" setup>
import { ElMessage } from "element-plus";
import { ref, watch } from "vue";

const emit = defineEmits(["update:modelValue"]);

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({}),
  },
});

const model = ref("");

watch(
  () => props.modelValue,
  (val) => {
    model.value = val ? JSON.stringify(val) : "";
  },
  { immediate: true }
);

function onChange(val: string) {
  try {
    const value = JSON.parse(val);
    emit("update:modelValue", value);
  } catch (err) {
    console.error(val, typeof val);
    ElMessage.error((err as Error).message);
  }
}
</script>

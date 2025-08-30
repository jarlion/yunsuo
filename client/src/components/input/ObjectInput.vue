<
<template>
  <el-input v-model="model" v-bind="$attrs" @change="onChange" />
</template>
<script lang="ts" setup>
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
  emit("update:modelValue", val);
}
</script>

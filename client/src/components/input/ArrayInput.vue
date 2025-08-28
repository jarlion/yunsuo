<template>
  <el-input v-for="i in index" v-model="model[i]" :key="i"/>
</template>
<script lang="ts" setup generic="T">
import { computed, defineModel, type PropType } from "vue";

const model = defineModel({
  type: Array as PropType<T[]>,
  default: () => [],
});

const index = computed(() => {
  const arr = model.value.map((v, i) => i);

  arr.push(model.value.length);
  return arr
});
</script>

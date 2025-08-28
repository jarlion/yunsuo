<template>
  <el-input v-model="model" />
</template>
<script lang="ts" generic="T">
import { defineModel, type PropType } from "vue";

const model = defineModel({
  type: Array as PropType<T[]>,
  default: () => [],
});
</script>

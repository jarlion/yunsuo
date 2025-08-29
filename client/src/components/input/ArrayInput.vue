<template>
  <el-input v-for="i in index" v-model="model[i]" :key="i" v-bind="$attrs">
    <template #append>
      <el-button :icon="Delete" @click="onDelete(i)" type="danger" />
    </template>
  </el-input>
</template>
<script lang="ts" setup generic="T">
import { computed, defineModel, type PropType } from "vue";
import { Delete } from "@element-plus/icons-vue";

const model = defineModel({
  type: Array as PropType<T[]>,
  default: () => [],
});

const index = computed(() => {
  const arr = model.value.map((v, i) => i);

  arr.push(model.value.length);
  return arr
});

function onDelete(i: number) {
  model.value.splice(i, 1);
}
</script>

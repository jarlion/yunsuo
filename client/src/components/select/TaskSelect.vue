<template>
  <el-select v-model="model" v-bind="$attrs">
    <el-option
      v-for="item in options"
      :key="item.value"
      :label="item.label"
      :value="item.value"
    />
  </el-select>
</template>

<script lang="ts" setup>
import { ref, onMounted, type ShallowRef } from "vue";
import { list } from "@/protocols/tasks/list";

const model = defineModel({
  type: String,
  default: "",
});

const options: ShallowRef<{ value: string; label: string }[]> = ref([]);

onMounted(async () => {
  const tasks = await list({});
  options.value = tasks.map((i) => ({
    value: i.code,
    label: i.name,
  }));
});
</script>

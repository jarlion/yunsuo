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
import type { ISelectOption } from "@/models/SelectOption";
import type { TaskManager } from "@/models/Task";
import { getSingleton } from "@/utils/singleton";
import { shallowRef, type ShallowRef } from "vue";

const model = defineModel({
  type: String,
  default: "",
});

const taskManager = getSingleton<TaskManager>("taskManager");
const options: ShallowRef<ISelectOption[]> = shallowRef([]);

async function initOptions() {
  await taskManager.init();
  options.value = taskManager.toOptions();
}

initOptions();
</script>

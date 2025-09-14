<template>
  <el-switch
    v-model="model"
    v-bind="$attrs"
  />
</template>
<script lang="ts" setup>
import { defineModel } from "vue";

const model = defineModel({
  type: Boolean,
  default: false,
});

</script>

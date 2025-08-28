<template>
  <el-input
    type="textarea"
    v-model="model"
    :autosize="{ minRows: 2, maxRows: 4 }"
  />
</template>
<script lang="ts" setup>
import { defineModel } from "vue";

const model = defineModel({
  type: String,
});
</script>

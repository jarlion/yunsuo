<template>
  <el-input v-model="model" v-bind="$attrs"/>
</template>
<script lang="ts" setup>
import { defineModel } from 'vue'

const model = defineModel({
  type: String,
});
</script>

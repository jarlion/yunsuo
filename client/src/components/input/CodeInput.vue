<template>
  <el-input type="textarea" v-model="model" />
</template>
<script lang="ts" setup>
import { defineModel } from 'vue'

const model = defineModel({
  type: String
})
</script>
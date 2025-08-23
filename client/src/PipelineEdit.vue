<template>
  <div class="pipeline-editor">
    <el-row :gutter="10" justify="end">
      <el-col :span="1">
        <el-button :icon="Delete" @click="onDeleteSelected()"></el-button>
      </el-col>
      <el-col :span="1">
        <el-button :icon="Plus" type="primary" @click="onEdit()"></el-button>
      </el-col>
    </el-row>
    <el-row :gutter="10">
      <el-col :span="24">
        <el-table ref="pipelineTblRef" :data="model" style="width: 100%">
          <el-table-column type="selection" width="55" />
          <el-table-column type="index" width="50" />
          <el-table-column prop="code" label="Code" width="100" />
          <el-table-column prop="name" label="Name" width="180" />
          <el-table-column prop="desc" label="Desc" show-overflow-tooltip />
          <el-table-column label="Stars" width="120">
            <template #default="{ row }">
              <el-icon v-for="s in createArr(0, row.stars)">
                <StarFilled />
              </el-icon>
              <el-icon v-for="s in createArr(row.stars, 5)">
                <Star />
              </el-icon>
            </template>
          </el-table-column>
          <el-table-column label="Actions" width="120">
            <template #default="{ row }">
              <el-button
                :icon="Edit"
                type="primary"
                size="small"
                @click="onEdit(row)"
              />
              <el-button
                :icon="Delete"
                type="danger"
                size="small"
                @click="onDelete([row])"
              />
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>
    <PipelineDialog ref="pipelineDlgRef" @ok="onOk" />
  </div>
</template>
<script setup lang="ts">
import { Delete, Edit, Plus, Star, StarFilled } from "@element-plus/icons-vue";
import { ref, shallowRef, type ShallowRef } from "vue";

import {
  ElButton,
  ElCol,
  ElIcon,
  ElMessage,
  ElMessageBox,
  ElRow,
  ElTable,
  ElTableColumn,
  type TableInstance,
} from "element-plus";
import PipelineDialog from "@/dialogs/PipelineDialog.vue";
import type { IPipeline } from "@/models/Pipeline";
import { del } from "@/protocols/pl/del";
import { list } from "@/protocols/pl/list";
import { add } from "@/protocols/pl/add";
import { update } from "@/protocols/pl/update";

const model: ShallowRef<IPipeline[]> = shallowRef([]);

const pipelineDlgRef = ref<typeof PipelineDialog>();

const pipelineTblRef = ref<TableInstance>();

function createArr(start: number = 0, end: number = 0) {
  return new Array(end - start).fill(true);
}

function onEdit(row?: IPipeline) {
  pipelineDlgRef.value?.show(row);
}

async function onDelete(rows: IPipeline[]) {
  console.log(rows);
  if (!rows?.length) {
    ElMessage.warning("请选择要删除的项");
    return;
  }

  try {
    await ElMessageBox.confirm("确定删除选中项吗？", "删除确认", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    });
  } catch {
    return;
  }
  try {
    const ids = rows.reduce((arr, p) => {
      if (p.id) {
        arr.push(p.id);
      }
      return arr;
    }, [] as string[]);
    model.value = await del(ids);
  } catch {
    return;
  }
}

async function onOk(pipeline: IPipeline) {
  const isCreate = model.value.find((p) => p.id === pipeline.id);
  try {
    if (isCreate === null) {
      model.value = await add(pipeline);
    } else {
      model.value = await update(pipeline);
    }
  } catch (err) {
    ElMessage.error((err as Error).message);
    return;
  }
}

async function onDeleteSelected() {
  const selection = pipelineTblRef.value?.getSelectionRows();
  console.log(selection);

  onDelete(selection as IPipeline[]);
}

async function init() {
  try {
    model.value = await list({});
    console.log(model.value);
  } catch (err) {
    ElMessage.error((err as Error).message);
  }
}

init();
</script>

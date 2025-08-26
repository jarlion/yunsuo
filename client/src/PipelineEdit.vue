<template>
  <div class="pipeline-editor">
    <div class="pipelist-table-title">
      <el-button-group class="ml-4">
        <el-button :icon="Delete" type="danger" @click="onDeleteSelected()" />
        <el-button :icon="Plus" type="primary" @click="onEdit()" />
      </el-button-group>
    </div>
    <el-row :gutter="10">
      <el-col :span="24">
        <el-table ref="pipelineTblRef" :data="model" style="width: 100%">
          <el-table-column type="selection" width="55" />
          <el-table-column type="index" width="50" />
          <el-table-column prop="code" label="Code" width="100" />
          <el-table-column prop="name" label="Name" width="180" />
          <el-table-column
            prop="desc"
            label="Description"
            show-overflow-tooltip
          />
          <el-table-column label="Stars" width="150">
            <template #default="{ row }">
              <el-rate v-model="row.stars" :colors="colors" />
            </template>
          </el-table-column>
          <el-table-column label="Actions" width="120">
            <template #default="{ row }">
              <el-button
                :icon="CaretRight"
                type="primary"
                link
                @click="onExec(row)"
              />
              <el-button :icon="Edit" link @click="onEdit(row)" />
              <el-button
                :icon="Delete"
                type="danger"
                link
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
import { CaretRight, Delete, Edit, Plus } from "@element-plus/icons-vue";
import {
  ElButton,
  ElCol,
  ElMessage,
  ElMessageBox,
  ElRow,
  ElTable,
  ElTableColumn,
  type TableInstance,
} from "element-plus";
import { ref, shallowRef, type ShallowRef } from "vue";

import PipelineDialog from "@/dialogs/PipelineDialog.vue";
import type { IPipeline } from "@/models/Pipeline";
import { add } from "@/protocols/pl/add";
import { del } from "@/protocols/pl/del";
import { list } from "@/protocols/pl/list";
import { update } from "@/protocols/pl/update";
import { exec } from "./protocols/pl/exec";

const model: ShallowRef<IPipeline[]> = shallowRef([]);

const pipelineDlgRef = ref<typeof PipelineDialog>();

const pipelineTblRef = ref<TableInstance>();

const colors = ref(["#99A9BF", "#F7BA2A", "#FF9900"]);

async function onExec(row: IPipeline) {
  try {
    const { id } = row;
    const result = await exec({
      id,
    });
    ElMessage.success("执行成功");
  } catch (err) {
    ElMessage.error((err as Error).message);
  }
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
  } catch (err) {
    ElMessage.error((err as Error).message);
  }
}

init();
</script>
<style lang="css">
.pipelist-table-title {
  display: flex;
  justify-content: flex-end;
}
</style>

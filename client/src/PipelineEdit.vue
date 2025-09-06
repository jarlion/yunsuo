<template>
  <div class="pipeline-editor">
    <ListEditPane
      v-model="model"
      :columns="columns"
      :width="1000"
      :height="500"
      @edit="onEdit"
      @delete="onDelete"
      @refresh="onRefresh"
    />
    <PipelineDialog ref="pipelineDlgRef" @ok="onOk" />
  </div>
</template>
<script setup lang="tsx">
import {
  CaretRight,
  CopyDocument,
  Delete,
  Edit,
  Plus,
  RefreshRight,
} from "@element-plus/icons-vue";
import {
  ElButton,
  ElMessage,
  ElMessageBox,
  type Column,
  ElTooltip,
} from "element-plus";
import { ref, reactive } from "vue";

import PipelineDialog from "@/dialogs/PipelineDialog.vue";
import ListEditPane from "@/components/panes/ListEditPane.vue";
import { clone, type IPipeline } from "@/models/Pipeline";
import { add } from "@/protocols/pl/add";
import { del } from "@/protocols/pl/del";
import { list } from "@/protocols/pl/list";
import { update } from "@/protocols/pl/update";
import { exec } from "@/protocols/pl/exec";
import { copy } from "@/protocols/pl/copy";

const model = ref<(IPipeline & { checked: boolean })[]>([]);

const pipelineDlgRef = ref<typeof PipelineDialog>();

const colors = ref(["#99A9BF", "#F7BA2A", "#FF9900"]);

// 定义表格列配置
const columns: Column<IPipeline & { checked: boolean }>[] = [
  {
    key: "index",
    dataKey: "index",
    title: "Index",
    width: 70,
    cellRenderer: ({ rowIndex }) => rowIndex + 1,
  },
  {
    key: "id",
    dataKey: "id",
    title: "ID",
    width: 200,
    cellRenderer: ({ cellData }) => cellData,
  },
  {
    key: "name",
    dataKey: "name",
    title: "Name",
    width: 180,
  },
  {
    key: "desc",
    dataKey: "desc",
    title: "Description",
    width: 250,
  },
  {
    key: "stars",
    dataKey: "stars",
    title: "Stars",
    width: 150,
    cellRenderer: ({ rowData }) => (
      <el-rate
        v-model={rowData.stars}
        colors={colors.value}
        onChange={(s: number) => onChangeStars(rowData, s)}
      />
    ),
  },
  {
    key: "actions",
    title: "Actions",
    width: 200,
    cellRenderer: ({ rowData }) => (
      <div style="display: flex; gap: 8px;">
        <ElButton
          icon={CaretRight}
          type="primary"
          link
          onClick={() => onExec(rowData)}
        />
        <ElButton icon={Edit} link onClick={() => onEdit(rowData)} />
        <ElButton icon={CopyDocument} link onClick={() => onCopy(rowData)} />
        <ElButton
          icon={Delete}
          type="danger"
          link
          onClick={() => onDelete([rowData])}
        />
      </div>
    ),
  },
];

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

async function onAdd() {
  try {
    const pipeline = await add();
    model.value.push({
      ...pipeline,
      checked: false,
    });
    return pipeline;
  } catch (err) {
    ElMessage.error((err as Error).message);
  }
}

async function onEdit(row?: IPipeline) {
  if (!row) {
    row = await onAdd();
  }
  pipelineDlgRef.value?.show(row);
}

async function onCopy(row: IPipeline) {
  if (!row?.id) {
    ElMessage.error("请先保存流水线");
    return;
  }
  try {
    const newPipeline = await copy(row.id);
    onEdit(newPipeline);
  } catch (err) {
    ElMessage.error((err as Error).message);
  }
}

async function onChangeStars(row: IPipeline, stars: number) {
  row.stars = stars;
  try {
    model.value = (
      await update({
        id: row.id,
        stars,
      })
    ).map((p) => ({ ...p, checked: false }));
  } catch (err) {
    ElMessage.error((err as Error).message);
  }
}

async function onRefresh() {
  try {
    const pipelines = await list({});
    // 将获取到的流水线数据转换为包含checked属性的格式
    model.value = pipelines.map((p) => ({ ...p, checked: false }));
  } catch (err) {
    ElMessage.error((err as Error).message);
  }
}

async function onDelete(rows: (IPipeline & { checked: boolean })[]) {
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
    const pipelines = await del(ids);
    model.value = pipelines.map((p) => ({ ...p, checked: false }));
  } catch {
    return;
  }
}

async function onOk(pipeline: IPipeline) {
  try {
    let pipelines = await update(pipeline);
    model.value = pipelines.map((p) => ({ ...p, checked: false }));
  } catch (err) {
    ElMessage.error((err as Error).message);
    return;
  }
}

async function init() {
  try {
    const pipelines = await list({});
    model.value = pipelines.map((p) => ({ ...p, checked: false }));
  } catch (err) {
    ElMessage.error((err as Error).message);
  }
}

init();
</script>
<style lang="css">
.pipeline-editor {
  padding: 16px;
}
</style>

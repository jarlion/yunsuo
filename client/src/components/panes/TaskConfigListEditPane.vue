<template>
  <ListEditPane
    :columns="columns"
    v-model="model"
    @delete="onDelete"
    @edit="onEdit"
  />
  <TaskDialog ref="taskDialogRef" :ctx="ctx" />
</template>
<script setup lang="tsx">
import { Bottom, Delete, Operation, Top } from "@element-plus/icons-vue";
import { ElButton, ElMessage, ElSwitch, type Column } from "element-plus";
import { ref, type PropType } from "vue";

import ListEditPane from "@/components/panes/ListEditPane.vue";
import TaskDialog from "@/dialogs/TaskDialog.vue";
import { initRecord, TaskManager, type ITaskConfig } from "@/models/Task";
import { add } from "@/protocols/task/add";
import { del } from "@/protocols/task/del";
import { getSingleton } from "@/utils/singleton";
import { list } from "@/protocols/pl/task/list";

interface ITaskConfigRow extends ITaskConfig {
  checked: boolean;
}

const props = defineProps({
  ctx: {
    type: Object as PropType<Record<string, any>>,
    default: () => ({}),
  },
  pipelineId: {
    type: String,
    default: "",
  },
});

const taskDialogRef = ref();

const model = defineModel({
  type: Array as PropType<ITaskConfigRow[]>,
  default: [],
});

const initParams = (code: string, rowData: ITaskConfigRow) => {
  if (!code) {
    return;
  }
  const task = getSingleton<TaskManager>("taskManager")?.getTask(code);
  if (task) {
    rowData.params = initRecord(task.params);
  }
};

const columns: Column<any>[] = [
  {
    key: "index",
    title: "Index",
    width: 70,
    cellRenderer: ({ rowIndex }) => <span>{rowIndex + 1}</span>,
  },
  {
    key: "code",
    title: "Code",
    dataKey: "code",
    width: 120,
    cellRenderer: ({ rowData }) => rowData.code,
  },
  {
    key: "desc",
    title: "Description",
    dataKey: "desc",
    width: 200,
    cellRenderer: ({ rowData }) => <p>{getTaskDescription(rowData.code)}</p>,
  },
  {
    key: "on",
    title: "On",
    dataKey: "on",
    width: 80,
    cellRenderer: ({ rowData }) => <ElSwitch v-model={rowData.on} />,
  },
  {
    key: "operations",
    title: "Operations",
    cellRenderer: ({ rowData, rowIndex }) => (
      <>
        <ElButton
          icon={Operation}
          link
          onClick={(e) => {
            onEdit(rowData);
          }}
        />
        <ElButton
          icon={Top}
          link
          onClick={(e) => {
            e.stopPropagation();
            moveTaskBy(rowIndex, -1);
          }}
        />
        <ElButton
          icon={Bottom}
          link
          onClick={(e) => {
            e.stopPropagation();
            moveTaskBy(rowIndex, 1);
          }}
        />
        <ElButton
          icon={Delete}
          link
          type="danger"
          onClick={(e) => {
            e.stopPropagation();
            onDelete([rowData]);
          }}
        />
      </>
    ),
    width: 130,
  },
];

function moveTaskBy(index: number, offset: number) {
  const newIndex = index + offset;
  if (newIndex < 0 || newIndex >= model.value.length) {
    return;
  }
  const temp = model.value[index];
  model.value[index] = model.value[newIndex];
  model.value[newIndex] = temp;
}

function getTaskDescription(code: string) {
  const task = getSingleton<TaskManager>("taskManager")?.getTask(code);
  return task?.desc || "";
}

async function onDelete(rows: ITaskConfigRow[]) {
  const ids = rows.map((i) => i.id);
  try {
    await del(ids)
    model.value = (await list({ pl_id: props.pipelineId })).map((i) => ({ ...i, checked: false }));
    // model.value = (await del(ids)).map((i) => ({ ...i, checked: false }));
  } catch (err) {
    ElMessage.error((err as Error).message);
  }
}

async function onEdit(row: ITaskConfig) {
  try {
    let tc = row;
    if (!tc) {
      tc = await add(props.pipelineId);
      model.value.push({ ...tc, checked: false });
    }
    taskDialogRef.value.show(tc);
  } catch (err) {
    ElMessage.error((err as Error).message);
  }
}
</script>

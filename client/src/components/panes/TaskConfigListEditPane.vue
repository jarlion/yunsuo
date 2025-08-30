<template>
  <ListEditPane
    :columns="columns"
    v-model="model"
    @delete="onDelete"
    @edit="onEdit"
    />
  </template>
<script setup lang="tsx">
import { Bottom, Delete, Top } from "@element-plus/icons-vue";
import { ElButton, ElSwitch, type Column } from "element-plus";
import { type PropType } from "vue";

import ListEditPane from "@/components/panes/ListEditPane.vue";
import TaskTestPopover from "@/components/popover/TaskTestPopover.vue";
import TaskSelect from "@/components/select/TaskSelect.vue";
import {
  initRecord,
  TaskManager,
  type ITaskConfig
} from "@/models/Task";
import { getSingleton } from "@/utils/singleton";

interface ITaskConfigRow extends ITaskConfig {
  checked: boolean;
}

const props = defineProps({
  ctx: {
    type: Object as PropType<Record<string, any>>,
    default: () => ({}),
  },
});

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
    width: 200,
    cellRenderer: ({ rowData }) => (
      <TaskSelect
        v-model={rowData.code}
        onUpdate:modelValue={(v) => initParams(v, rowData)}
      />
    ),
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
    width: 200,
    cellRenderer: ({ rowData }) => <ElSwitch v-model={rowData.on} />,
  },
  {
    key: "operations",
    title: "Operations",
    cellRenderer: ({ rowData,rowIndex }) => (
      <>
        <TaskTestPopover
          code={rowData.code}
          v-model={rowData.params}
          ctx={props.ctx}
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
    width: 150,
    align: "center",
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
  model.value = model.value.filter((i) => !ids.includes(i.id));
}

async function onEdit(row: ITaskConfigRow) {
  if (!row) {
    model.value.push({
      id: new Date().getTime().toString(),
      checked: false,
      code: "",
      params: [],
    });
    return;
  }
}
</script>

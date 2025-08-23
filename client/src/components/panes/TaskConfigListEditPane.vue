<template>
  <ListEditPane
    :columns="columns"
    v-model="model"
    @delete="onDelete"
    @edit="onEdit"
  />
</template>
<script setup lang="tsx">
import ListEditPane from "@/components/panes/ListEditPane.vue";
import { type IDefValue, type ITaskConfig } from "@/models/Task";
import {
  ElButton,
  ElTag,
  ElTooltip,
  type CheckboxValueType,
  type Column,
} from "element-plus";
import { type PropType } from "vue";
import TaskSelect from "../select/TaskSelect.vue";
import { Delete, Edit } from "@element-plus/icons-vue";

interface ITaskConfigRow extends ITaskConfig {
  checked: boolean;
}

const model = defineModel({
  type: Array as PropType<ITaskConfigRow[]>,
  default: [],
});

const ParamsCellRender = ({ cellData }: { cellData: IDefValue[] }) => {
  if (!cellData) {
    return <p>--</p>;
  }
  const keys = cellData;
  const more = keys.length > 1 ? `+${keys.length - 1}` : "";
  return (
    <ElTooltip content={keys.map((i) => `${i.name}:${i.type}`).join(",")}>
      {
        <div>
          {[
            keys[0] && <ElTag>{`${keys[0].name}:${keys[0].type}`}</ElTag>,
            more && <ElTag>{more}</ElTag>,
          ]}
        </div>
      }
    </ElTooltip>
  );
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
      <TaskSelect v-model={rowData.code}></TaskSelect>
    ),
  },
  {
    key: "params",
    title: "Params",
    dataKey: "params",
    width: 200,
    // cellRenderer: ParamsCellRender,
  },
  {
    key: "operations",
    title: "Operations",
    cellRenderer: ({ rowData }) => (
      <>
        <ElButton icon={Edit} link></ElButton>
        <ElButton
          icon={Delete}
          link
          type="danger"
          onClick={(e) => {
            e.stopPropagation();
            onDelete([rowData]);
          }}
        >
        </ElButton>
      </>
    ),
    width: 150,
    align: "center",
  },
];

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

// async function init() {
//   try {
//     model.value = await list({});
//   } catch (err) {
//     ElMessage.error((err as Error).message);
//   }
// }

// init();
</script>

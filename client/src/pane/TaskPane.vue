<template>
  <el-table-v2 :columns="columns" :data="model" :width="700" :height="400" />
</template>

<script lang="tsx" setup>
import { ElButton, ElMessage, ElTag, ElTooltip } from "element-plus";
import { shallowRef, type ShallowRef } from "vue";

import type { IDefValue, ITask } from "@/model/Task";
import { list } from "@/protocols/tasks/list";
import type { Column } from "element-plus";
import { TableV2FixedDir } from "element-plus";

const ParamsCellRender = ({ cellData }: { cellData: IDefValue[] }) => {
  if (!cellData) {
    return <p>--</p>;
  }
  const keys = cellData;
  const more = keys.length > 1 ? `+${keys.length - 1}` : "";
  return (
    <ElTooltip content={keys.map((i) => `${i.name}:${i.type}`).join(',')}>
      {
        <div>
          {[
            keys[0]&&<ElTag>{`${keys[0].name}:${keys[0].type}`}</ElTag>,
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
    key: "name",
    title: "Name",
    dataKey: "name",
    width: 200,
    cellRenderer: ({ cellData: name }) => (
      <ElTooltip content={name}>{name}</ElTooltip>
    ),
  },
  {
    key: "ctx",
    title: "Context",
    dataKey: "ctx",
    width: 200,
    cellRenderer: ParamsCellRender,
  },
  {
    key: "params",
    title: "Params",
    dataKey: "params",
    width: 200,
    cellRenderer: ParamsCellRender,
  },
  {
    key: "result",
    title: "Result",
    dataKey: "result",
    width: 200,
    cellRenderer: ParamsCellRender,
  },
  {
    key: "operations",
    title: "Operations",
    cellRenderer: () => (
      <>
        <ElButton size="small">Edit</ElButton>
        <ElButton size="small" type="danger">
          Delete
        </ElButton>
      </>
    ),
    width: 150,
    align: "center",
  },
];

const model: ShallowRef<ITask[]> = shallowRef([
]);

async function init() {
  try {
    model.value = await list({});
  } catch (err) {
    ElMessage.error((err as Error).message);
  }
}

  init();
</script>

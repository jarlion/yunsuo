<template>
  <el-table-v2 :columns="columns" :data="model" :width="700" :height="400" />
</template>

<script lang="tsx" setup>
import { ElButton, ElIcon, ElTag, ElTooltip } from "element-plus";
import { ref, shallowRef, type ShallowRef } from "vue";

import type { Column } from "element-plus";
import type { ITask } from "@/model/Task";
import { TableV2FixedDir } from "element-plus";

const ParamsCellRender = ({ cellData }) => {
  if (!cellData) {
    return <p>--</p>;
  }
  const keys = Object.keys(cellData);
  const more = keys.length > 1 ? `+${keys.length - 1}` : "";
  return (
    <ElTooltip content={keys.join(',')}>
      {
        <div>
          {[
            <ElTag>{`${keys[0]}:${cellData[keys[0]]}`}</ElTag>,
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
    width: 60,
    fixed: TableV2FixedDir.LEFT,
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
  {
    id: "1",
    code: "OpenFileOrDir",
    desc: "打开文件/文件夹",
    name: "打开文件/文件夹",
    mode: "1",
    params: { path: "str", encode: "str" },
    ctx: { root: "str" },
    result: { file: "any", dir: "any" },
  },
]);
</script>

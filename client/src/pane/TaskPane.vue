<template>
  <el-table-v2
    :columns="columns"
    :data="data"
    :width="700"
    :height="400"
  />
</template>

<script lang="tsx" setup>
import { Timer } from '@element-plus/icons-vue'
import {
    ElButton,
    ElIcon,
    ElTag,
    ElTooltip,
} from 'element-plus'
import { ref } from 'vue'

import type { Column } from 'element-plus'
import { TableV2FixedDir } from 'element-plus'

let id = 0

const dataGenerator = () => ({
  id: `random-id-${++id}`,
  name: 'Tom',
  date: '2020-10-1',
})

const columns: Column<any>[] = [
  {
    key: 'date',
    title: 'Date',
    dataKey: 'date',
    width: 150,
    fixed: TableV2FixedDir.LEFT,
    cellRenderer: ({ cellData: date }) => (
      <ElTooltip content="2020/10/1">
        {
          <span class="flex items-center">
            <ElIcon class="mr-3">
              <Timer />
            </ElIcon>
          </span>
        }
      </ElTooltip>
    ),
  },
  {
    key: 'name',
    title: 'Name',
    dataKey: 'name',
    width: 150,
    align: 'center',
    cellRenderer: ({ cellData: name }) => <ElTag>{name}</ElTag>,
  },
  {
    key: 'operations',
    title: 'Operations',
    cellRenderer: () => (
      <>
        <ElButton size="small">Edit</ElButton>
        <ElButton size="small" type="danger">
          Delete
        </ElButton>
      </>
    ),
    width: 150,
    align: 'center',
  },
]

const data = ref(Array.from({ length: 200 }).map(dataGenerator))
</script>
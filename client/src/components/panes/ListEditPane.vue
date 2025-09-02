<template>
  <div class="ys-align-right">
    <el-button-group>
      <el-button :icon="RefreshRight" @click="onRefresh()" />
      <el-button :icon="Delete" type="danger" @click="onDeleteSelected()" />
      <el-button :icon="Plus" type="primary" @click="onEdit()" />
    </el-button-group>
  </div>
  <div :style="`height: ${height}px`">
    <el-auto-resizer>
      <template #default="{ height: h, width: w }">
        <el-table-v2
          ref="tblRef"
          :columns="editedColumns"
          :data="model"
          :width="w"
          :height="h"
          :expand-column-key="expandColumnKey"
        />
      </template>
    </el-auto-resizer>
  </div>
</template>

<script
  lang="tsx"
  setup
  generic="T extends { checked: boolean, children?: T[] }"
>
import { type SelectionCellProps } from "@/components/tables/cells/TableCell";
import { Delete, Plus, RefreshRight } from "@element-plus/icons-vue";
import {
  ElCheckbox,
  ElMessage,
  ElMessageBox,
  type CheckboxValueType,
  type Column,
  type TableInstance,
} from "element-plus";
import {
  computed,
  ref,
  unref,
  type FunctionalComponent,
  type PropType,
} from "vue";

const emit = defineEmits(["edit", "delete", "refresh"]);

const props = defineProps({
  columns: {
    type: Array as PropType<Column<any>[]>,
    default: () => [],
  },
  expandColumnKey: {
    type: String,
  },
  width: {
    type: Number,
    default: 500,
  },
  height: {
    type: Number,
    default: 300,
  },
  onChange: {
    type: Function as PropType<(selection: T[]) => void>,
    default: () => {},
  },
});

const model = defineModel({
  type: Array as PropType<T[]>,
  default: () => [],
});

const tblRef = ref<TableInstance>();

function onRefresh() {
  emit("refresh");
}

function onEdit(row?: T) {
  emit("edit", row);
}

async function onDelete(rows: T[]) {
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
    emit("delete", rows);
  } catch {
    return;
  }
}

async function onDeleteSelected() {
  const selection = model.value.filter((i) => i.checked);
  onDelete(selection);
}

const SelectionCell: FunctionalComponent<SelectionCellProps> = ({
  value,
  intermediate = false,
  onChange,
}) => {
  return (
    <ElCheckbox
      onChange={onChange}
      modelValue={value}
      indeterminate={intermediate}
    />
  );
};

const editedColumns = computed(() => {
  return [
    {
      key: "selection",
      width: 40,
      cellRenderer: ({ rowData }: { rowData: T }) => {
        const onChange = (value: CheckboxValueType) =>
          (rowData.checked = Boolean(value));
        return <SelectionCell value={rowData.checked} onChange={onChange} />;
      },
      headerCellRenderer: () => {
        const _data = unref(model);
        const onChange = (value: CheckboxValueType) =>
          (model.value = _data.map((row) => {
            row.checked = Boolean(value);
            return row;
          }));
        const allSelected = _data.every((row) => row.checked);
        const containsChecked = _data.some((row) => row.checked);

        return (
          <SelectionCell
            value={allSelected}
            intermediate={containsChecked && !allSelected}
            onChange={onChange}
          />
        );
      },
    },
    ...props.columns,
  ];
});
</script>

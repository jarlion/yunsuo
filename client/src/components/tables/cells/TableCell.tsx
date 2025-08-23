import { ElCheckbox, type CheckboxValueType } from "element-plus";
import type { FunctionalComponent } from "vue";

export interface SelectionCellProps {
  value: CheckboxValueType;
  intermediate?: boolean;
  onChange?: (value: CheckboxValueType) => void;
}
export const SelectionCell: FunctionalComponent<SelectionCellProps> = ({
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
  )
}
import { request } from "@/conn/Connection";
import type { ITaskConfig } from "@/models/Task";

export function del(ids: string[]) {
  return request<ITaskConfig[], string[]>({
    url: "task/del",
    params: ids,
  });
}

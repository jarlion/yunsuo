import { request } from "@/conn/Connection";
import type { ITaskConfig } from "@/models/Task";

export function add(pl_id: string) {
  return request<ITaskConfig, { pl_id: string }>({
    url: "task/add",
    params: {
      pl_id,
    },
  });
}

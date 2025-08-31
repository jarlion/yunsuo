import { request } from "@/conn/Connection";
import type { ITaskConfig } from "@/models/Task";

export function update(task: Partial<ITaskConfig>) {
  return request<ITaskConfig[], Partial<ITaskConfig>>({
    url: "task/update",
    params: task,
  });
}

import { request } from "@/conn/Connection";
import type { ITaskConfig } from "@/models/Task";
import type { ITaskParams } from "@/protocols/base/ITaskParams";

export function update(task: Partial<ITaskParams>) {
  return request<ITaskConfig[], Partial<ITaskParams>>({
    url: "task/update",
    params: task,
  });
}

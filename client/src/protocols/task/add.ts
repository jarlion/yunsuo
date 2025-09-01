import { request } from "@/conn/Connection";
import type { ITaskConfig } from "@/models/Task";

export function add(params: IAddTaskParams) {
  return request<ITaskConfig, IAddTaskParams>({
    url: "task/add",
    params,
  });
}

export interface IAddTaskParams {
  pl_id: string;
  pid?: string;
}

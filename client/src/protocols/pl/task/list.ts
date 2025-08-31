import { request } from "@/conn/Connection";
import type { ITaskConfig } from "@/models/Task";

export function list(params: IListParams) {
  return request<ITaskConfig[], IListParams>({
    url: "pl/task/list",
    params,
  });
}

export interface IListParams {
  pl_id: string;
}

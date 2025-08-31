import type { ITask } from "@/models/Task";
import { request } from "@/conn/Connection";

export function list(params: IListParams) {
  return request<ITask[], IListParams>({
    url: "task/list",
    params,
  });
}

export interface IListParams {
  code?: string;
}

import type { ITask } from "@/model/Task";
import { request } from "../../conn/Connection";

export function list(params: IListParams) {
  return request<ITask[], IListParams>({
    url: "task/list",
    params,
  });
}

export interface IListParams {
  code?: string;
}

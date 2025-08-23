import type { IPipeline } from "@/models/Pipeline";
import { request } from "../../conn/Connection";

export function list(params: IListParams) {
  return request<IPipeline[], IListParams>({
    url: "pl/list",
    params,
  });
}

export interface IListParams {
  code?: string;
  desc?: string;
  name?: string;
}

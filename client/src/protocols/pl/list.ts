import type { IPipeline } from "@/model/Pipeline";
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

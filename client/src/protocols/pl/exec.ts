import type { IPipeline } from "@/models/Pipeline";
import { request } from "@/conn/Connection";

export function exec(params: IExecParams) {
  return request<IPipeline, IExecParams>({
    url: "pl/exec",
    params,
  });
}

export interface IExecParams {
  id?: string;
}

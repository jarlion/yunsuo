import { request } from "@/conn/Connection";

export function exec(params: IExecParams) {
  return request<string[], IExecParams>({
    url: "pl/exec",
    params,
  });
}

export interface IExecParams {
  id?: string;
}

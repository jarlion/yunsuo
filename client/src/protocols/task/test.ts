import { request } from "@/conn/Connection";

export function test(params: ITaskTestParams) {
  return request<any, ITaskTestParams>({
    url: "task/test",
    params,
  });
}

export interface ITaskTestParams {
  code?: string;
  ctx?: Record<string, any>;
  params?: Record<string, any>;
}

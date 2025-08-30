import type { IPipeline } from "@/models/Pipeline";
import { request } from "@/conn/Connection";

export function del(ids: string[]) {
  return request<IPipeline[], string[]>({
    url: "pl/del",
    params: ids,
  });
}

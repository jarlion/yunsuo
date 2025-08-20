import type { IPipeline } from "@/model/Pipeline";
import { request } from "../../conn/Connection";

export function del(ids: string[]) {
  return request<IPipeline[], string[]>({
    url: "pl/delete",
    params: ids,
  });
}

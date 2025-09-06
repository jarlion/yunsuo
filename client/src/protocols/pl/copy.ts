import type { IPipeline } from "@/models/Pipeline";
import { request } from "@/conn/Connection";

export function copy(id: string) {
  return request<IPipeline, { id: string }>({
    url: "pl/copy",
    params: {
      id,
    },
  });
}

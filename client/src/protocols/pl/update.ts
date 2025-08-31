import type { IPipeline } from "@/models/Pipeline";
import { request } from "@/conn/Connection";

export function update(pl: Partial<IPipeline>) {
  return request<IPipeline[], Partial<IPipeline>>({
    url: "pl/update",
    params: pl,
  });
}

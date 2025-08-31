import type { IPipeline } from "@/models/Pipeline";
import { request } from "@/conn/Connection";

export function add() {
  return request<IPipeline, IPipeline>({
    url: "pl/add",
  });
}

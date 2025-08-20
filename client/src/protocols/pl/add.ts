import type { IPipeline } from "@/model/Pipeline";
import { request } from "../../conn/Connection";

export function add(pl: IPipeline) {
  return request<IPipeline[], IPipeline>({
    url: "pl/add",
    params: pl,
  });
}

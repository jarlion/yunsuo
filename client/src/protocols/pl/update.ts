import type { IPipeline } from "@/model/Pipeline";
import { request } from "../../conn/Connection";

export function update(pl: IPipeline) {
  return request<IPipeline[], IPipeline>({
    url: "pl/update",
    params: pl,
  });
}

import { request } from "@/conn/Connection";
import type { ITaskConfig } from "@/models/Task";

export function add() {
  return request<ITaskConfig, {}>({
    url: "task/add",
  });
}

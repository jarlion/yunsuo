import type { ITaskConfig } from "@/models/Task";

export interface ITaskParams {
  id: string;
  pid?: string;
  pl_id: string;
  code: string;
  on: boolean;
  params: any;
}

export function toTaskParams(task: ITaskConfig): ITaskParams {
  return {
    id: task.id,
    pid: task.parentId,
    pl_id: task.pipelineId,
    code: task.code,
    on: task.on,
    params: task.params,
  }
}
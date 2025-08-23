import type { ITaskConfig } from "./Task";

export interface IPipeline {
  id?: string;
  code: string;
  desc: string;
  name: string;
  stars: number;
  tasks: ITaskConfig[];
}

export function clone(pipeline: IPipeline): IPipeline {
  const { id, code, desc, name, stars, tasks } = pipeline;
  const clonedTasks = tasks.map((item) => ({
    ...item,
  }));
  return {
    id,
    code,
    desc,
    name,
    stars,
    tasks: clonedTasks,
  };
}

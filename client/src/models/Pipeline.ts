import type { ITaskConfig } from "./Task";

export interface IPipeline {
  id?: string;
  code: string;
  ctx: Record<string, string>;
  desc: string;
  name: string;
  stars: number;
  tasks: ITaskConfig[];
}

export function create(): IPipeline {
  return {
    id:  `PL${Date.now()}`,
    name: "",
    code: "",
    ctx: {},
    desc: "",
    stars: 0,
    tasks: [],
  };
}

export function clone(pipeline: IPipeline): IPipeline {
  const { id, code, ctx, desc, name, stars, tasks } = pipeline;
  const clonedTasks = tasks.map((item) => ({
    ...item,
  }));
  return {
    id,
    code,
    ctx,
    desc,
    name,
    stars,
    tasks: clonedTasks,
  };
}

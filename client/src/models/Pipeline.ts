import type { ITask } from "./Task";

export interface IPipeline {
    id?:string;
  code: string;
  desc: string;
  name: string;
  stars: number;
  tasks: ITask[];
}

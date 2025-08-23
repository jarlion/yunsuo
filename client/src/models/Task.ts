import { list } from "@/protocols/tasks/list";


export interface IDefValue {
  name: string;
  type: string;
  required: boolean;
  desc: string;
  default?: string;
}

export interface ITask {
  id: string;
  code: string;
  desc?: string;
  name: string;
  mode?: string;
  params: IDefValue[];
  ctx?: IDefValue[];
  result?: IDefValue[];
}

export interface ITaskConfig {
  id: string;
  code: string;
  params: IDefValue[];
}

export class TaskManager {
  private tasks: ITask[] = [];

  async init() {
    if (this.tasks.length > 0) {
      return this;
    }
    try {
      const tasks = await list({});
      this.tasks = tasks;
    } catch (err) {
      console.error('初始化任务失败', err);
    }
    return this;
  }
  
  toOptions() {
    return this.tasks.map((item) => ({
      value: item.code,
      label: item.name,
    }));
  }
}
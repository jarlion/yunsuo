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
  params: Record<string, any>;
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
      console.error("初始化任务失败", err);
    }
    return this;
  }

  getTask(code: string): ITask | undefined {
    return this.tasks.find((item) => item.code === code);
  }

  toOptions() {
    return this.tasks.map((item) => ({
      value: item.code,
      label: item.name,
    }));
  }
}

export function getComponent(task:ITask, prop:string) {
  const type =task.params?.find(p=>p.name===prop)?.type
  if (!type) {
    return 'TextInput';
  }
  if (type === "string") {
    return 'TextInput';
  }
  if (type === "code") {
    return 'CodeInput';
  }
}

export function initRecord(defs: IDefValue[]): Record<string, any> {
  const result: Record<string, any> = {};
  defs.forEach((def) => {
    result[def.name] = initRecordValue(def);
  });
  return result;
}

function initRecordValue(def: IDefValue) {
  if (def.default) {
    return def.default;
  }
  if (def.type === "string") {
    return "";
  }
  if (def.type === "code") {
    return "";
  }
  if (def.type === "number") {
    return 0;
  }
  if (def.type === "boolean") {
    return false;
  }
  if (def.type === "object") {
    return {};
  }
  if (def.type === "array" || def.type.endsWith("[]")) {
    return [];
  }
}

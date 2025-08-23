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
  desc: string;
  name: string;
  mode: string;
  params: IDefValue[];
  ctx: IDefValue[];
  result: IDefValue[];
}

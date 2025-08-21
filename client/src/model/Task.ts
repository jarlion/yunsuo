export interface ITask {
  id:string;
  code: string;
  desc: string;
  name: string;
  mode: string;
  params: Record<string, string>;
  ctx: Record<string, string>;
  result: Record<string, string>;
}

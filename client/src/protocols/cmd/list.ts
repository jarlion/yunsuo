import { request } from "../../conn/Connection";
import type { IPageParams } from "../base/IPageParams";

export function list(params: IListParams) {
  return request({
    url: "cmd/list",
    params,
  });
}

export interface IListParams {
  nameOrCode?: string;
  page: IPageParams;
}

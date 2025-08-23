import axios, { type AxiosResponse } from "axios";

const conn = axios.create({
  baseURL: "http://localhost:5000/",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

interface IResonse<T> {
  code: string;
  msg: string;
  data: T;
}

function parseResult<D,E>(res: AxiosResponse<IResonse<D>,E>) {
  if (res.data.code !== 'success') {
    throw new Error(res.data.msg);
  }
  return res.data.data;
}

export function request<R, P>(cfg: {
  url: string;
  method?: string;
  params?: P;
}) {
  if (!cfg.method) {
    cfg.method = "POST";
  }

  return conn
    .request<R, AxiosResponse<IResonse<R>, Error>, P>({
      ...cfg,
      data: cfg.params,
    })
    .then<R>(parseResult);
}
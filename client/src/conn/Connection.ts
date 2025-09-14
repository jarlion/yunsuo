import axios, { type AxiosResponse } from "axios";

const conn = axios.create({
  baseURL: "http://localhost:5000/",
  timeout: 100000,
  headers: {
    "Content-Type": "application/json;charset=utf-8",
  },
});

interface IMessage {
  success: (msg: string) => void;
  error: (msg: string) => void;
}

let message!: IMessage;

interface IResonse<T> {
  code: string;
  msg: string;
  data: T;
}

function parseResult<D, E>(res: AxiosResponse<IResonse<D>, E>) {
  if (res.data.code !== "success") {
    throw new Error(res.data.msg);
  }
  if (res.data.msg) {
    message?.success(res.data.msg);
  }
  return res.data.data;
}

export function init(message: IMessage) {
  message = message;
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

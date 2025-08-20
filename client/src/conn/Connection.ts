import axios, { type AxiosResponse } from "axios";

const conn = axios.create({
  baseURL: "http://localhost:5000/",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

export function request<T, P>(cfg: {
  url: string;
  method?: string;
  params?: P;
}): Promise<T> {
  if (!cfg.method) {
    cfg.method = "POST";
  }

  return conn
    .request<T, AxiosResponse<T, Error>, P>({
      ...cfg,
      data: cfg.params,
    })
    .then((res) => res.data);
}

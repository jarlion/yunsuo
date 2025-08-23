export interface ISingleton<T> {
  getInstance(): T;
}

const instances:Record<string, any> = {}

export function createSingleton<T>(instance: T, alias: string): T {
  instances[alias] = instance;
  return instance;
}

export function getSingleton<T>(alias: string): T {
  return instances[alias];
}
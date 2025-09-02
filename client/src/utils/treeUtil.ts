interface IInitTreeOptions<T> {
  data: T[];
  dataKey: keyof T;
  parentKey: keyof T;
}

export function initTree<
  T extends { children?: T[]; checked?: boolean },
  K extends keyof T,
  P extends keyof T
>({
  data,
  dataKey = "id" as K,
  parentKey = "parentId" as P,
}: IInitTreeOptions<T>): T[] {
  const tree: T[] = [];
  const childrenMap: Record<string | number, T[]> = {};

  for (const datum of data) {
    const item = { ...datum };
    const id = item[dataKey] as unknown as string | number;
    const parentId = item[parentKey] as unknown as string | number;

    if (Array.isArray(item.children)) {
      childrenMap[id] = item.children.concat(childrenMap[id] || []);
    } else if (!childrenMap[id]) {
      childrenMap[id] = [];
    }
    item.children = childrenMap[id];

    if (parentId) {
      if (!childrenMap[parentId]) childrenMap[parentId] = [];
      childrenMap[parentId].push(item);
    } else {
      tree.push(item);
    }
  }

  return tree;
}

// Vue单文件组件类型声明
declare module '*.vue' {
  import { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

// 额外的Vue组件相关类型
export type VueComponentProps<T extends any> = T extends { props: infer P } ? P : never

// 确保路径别名能够被TypeScript正确解析
declare module '@/*' {
  // 这里的声明是为了告诉TypeScript '@/*' 路径是有效的
  const module: any
  export default module
}

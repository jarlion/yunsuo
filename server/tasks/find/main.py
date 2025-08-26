import os
import re
from typing import List, Dict, Any


def main(params:Dict[str, Any], ctx:Dict[str, Any])->List[str]:
    root = ctx.get('root')
    # 正则表达式数组
    patterns = params.get('patterns', '[.+]')
    if not root:
        raise ValueError("Missing required params: root")
    if not patterns:
        raise ValueError("Missing required params: patterns")

    result = scan_directory(root, patterns)
    return result


def scan_directory(root: str, patterns: List[str]) -> List[str]:
    # 将字符串 '[.+]' 转成列表 '[.+]' -> ['[.+'] 的容错处理
    if isinstance(patterns, str):
        patterns = [patterns.strip("[]")] if patterns.startswith("[") else [patterns]

    max_depth = len(patterns)
    result = []

    compiled = [re.compile(p) for p in patterns]

    def _walk(current: str, depth: int):
        if depth >= max_depth:
            return
        try:
            for name in os.listdir(current):
                full_path = os.path.join(current, name)
                # 用当前层对应的正则匹配（depth 从 0 开始）
                if depth < len(compiled) and compiled[depth].search(name):
                    result.append(full_path)
                # 如果是目录，继续深入
                if os.path.isdir(full_path):
                    _walk(full_path, depth + 1)
        except PermissionError:
            # 无权限目录直接跳过
            pass

    _walk(root, 0)
    return result

if __name__ == '__main__':
    params = {
        'patterns': '[.+]',
    }
    print(main(params, {'root': '/'}))
    params = {
        'patterns': '[/.py]',
    }
    print(main(params, {'root': '/'}))
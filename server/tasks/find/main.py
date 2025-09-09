import os
import re
from typing import List, Dict, Any
from pathlib import Path


def main(params:Dict[str, Any], ctx:Dict[str, Any])->List[str]:
    root = ctx.get('root', '')
    if not root:
        raise ValueError("Missing required params: root")
    root = Path(root)
    if not root.exists():
        raise ValueError("root not exists")
    types = params.get('types', ['file'])
    for type in types:
        if type not in ['file', 'dir']:
            raise ValueError(f"types must be file or dir")

    patterns = params.get('patterns', '[.+]')
    match_paths = []
    # 安全地编译正则表达式，处理可能的语法错误
    regexps = [re.compile(pattern) for pattern in patterns]

    for base, dirs, files in os.walk(root):
        if 'file' in types:
            for file in files:
                append_match_paths(match_paths, os.path.join(base, file), regexps)
        if 'dir' in types:
            for dir in dirs:
                append_match_paths(match_paths, os.path.join(base, dir), regexps)

    ctx['result'] = match_paths
    return match_paths


def append_match_paths(match_paths: List[str], path: str, regexps: List[re.Pattern]):
    # 如果没有有效的正则表达式，则不执行匹配
    if not regexps:
        return
    
    for regexp in regexps:
        if not regexp.search(path):
            break
    else:
        match_paths.append(path)


if __name__ == '__main__':

    dirs = main({'patterns':['B\\d{3}']}, {'root': 'v:\\'})
    print(dirs)
    # params = {
    #     'patterns': ['/.py'],
    # }
    # print(main(params, {'root': '/'}))

import os
import re
from typing import List, Dict, Any


def main(params:Dict[str, Any], ctx:Dict[str, Any])->List[str]:
    root = ctx.get('root', '')
    if not root:
        raise ValueError("Missing required params: root")
    
    patterns = params.get('patterns', '[.+]')
    match_paths = []
    # 安全地编译正则表达式，处理可能的语法错误
    regexps = [re.compile(pattern) for pattern in patterns]

    for base, dirs, files in os.walk(root):            
        for file in files:
            append_match_paths(match_paths, os.path.join(base, file), regexps)
        
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

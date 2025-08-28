import os
import re
from typing import List, Dict, Any

result = {}

def exec_script(script: str, source: Any, env: Dict[str, Any] | None = None) -> Any:
    if not env:
        env = globals()
    local_dict = { 'output':None, 'iter':source }
    exec(script, env, local_dict)
    return local_dict.get('output', None)

def main(params:Dict[str, Any], ctx:Dict[str, Any])->Dict[str, Any]:
    global result
    script = params.get('script', '')
    if not script:
        raise ValueError("Missing required params: script")
    
    source_str = params.get('source', '')
    if not source_str:
        raise ValueError("Missing required params: source")
    source = eval(source_str[1:], globals()) if source_str.startswith('>') else source_str
    
    results = []
    # 如果source是字符串，直接执行script
    if isinstance(source, str):
        results.append(exec_script(script, source))
    # 如果source是列表，遍历执行script  
    if isinstance(source, list):
        for item in source:
            result = exec_script(script, item)
            if result:
                results.append(result)

    result = {"result": results}
    return result


if __name__ == '__main__':
    result = {'path': ['v:\\B994', 'v:\\B994\\B994.AZ', 'v:\\B994\\B994.DN']}
    dirs = main({'source': ">result['path']", 'script': '''
if os.path.isfile(iter):
    output = iter + ".zip"
    os.rename(iter, output)
    '''}, {})
    print(dirs)


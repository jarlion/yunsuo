import os
import re
from typing import List, Dict, Any

def main(params:Dict[str, Any], ctx:Dict[str, Any])->Dict[str, Any]:
    global result
    script = params.get('script', '')
    if not script:
        raise ValueError("Missing required params: script")
    
    env = {'result': result}
    src = ctx.get('source', '')
    source = exec(src[1:], env) if src.startswith('>') else src
    
    res = []
    # 如果source是字符串，直接执行script
    if isinstance(source, str):
        res.append(exec(script[1:], env))
    # 如果source是列表，遍历执行script  
    if isinstance(source, list):
        for item in source:
            env['iter'] = item
            res.append(exec(script[1:], env))

    result = {"result": res}
    return result


if __name__ == '__main__':
    global result
    result = {'path': ['v:\\B994', 'v:\\B994\\B994.AZ', 'v:\\B994\\B994.DN']}
    dirs = main({'source': ">result['path']", 'script': '>print(result)'}, {})
    print(dirs)
    # params = {
    #     'patterns': ['/.py'],
    # }
    # print(main(params, {'root': '/'}))

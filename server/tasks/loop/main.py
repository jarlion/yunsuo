import os
import re
from typing import List, Dict, Any

def main(params:Dict[str, Any], ctx:Dict[str, Any])->List[Any]:
    exec_script =(ctx.get('exec_script'))
    if not exec_script:
        raise ValueError("Missing required params: exec_script")
    berfore_str = params.get('before')
    if not berfore_str:
        raise ValueError("Missing required params: before")
    condition_str = params.get('condition')
    if not condition_str:
        raise ValueError("Missing required params: condition")
    after_str = params.get('after')
    if not after_str:
        raise ValueError("Missing required params: after")
    _ctx = ctx.copy()
    _ctx['cd'] = []
    cd = exec_script(berfore_str, globals(), _ctx)
    while eval(condition_str, globals(), _ctx):
        result = exec_script(after_str, globals(), _ctx)
    return result

if __name__ == '__main__':
    def exec_script(script:str, globals:Dict[str, Any], locals:Dict[str, Any])->Any:
        return eval(script, globals, locals)
    result = ["v:\\v20250825100235\\六花 喝醉 战斗衔接  锤 击中踩点（邪王真眼） S1 .mp4"]
    params = {
        "before": "v:\\v20250825100235",
        "condition": ">len(cd)>0",
        "after": "cd=cd[1:]"
    }
    dirs = main(params, {"exec_script": exec_script, "result": result})
    print(dirs)
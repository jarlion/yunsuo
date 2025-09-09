import os
from pathlib import Path
from typing import Dict,Any

def main(params: Dict[str,str], ctx: Dict[str,Any])->str:
    path = params.get('path')
    new_name = params.get('new_name')
    rule = params.get('rule', '')
    if not path or not new_name:
        raise ValueError("Missing required params: path, new_name")
    if path.startswith('>'):
        path = eval(path[1:], globals(), ctx)
    try:
        result = rename(path, new_name, rule)
    except Exception as e:
        raise e
    print('rename result:', result)
    return result

def rename(path:str, new_name:str, rule:str)->str:
    p = Path(path)

    if rule == 'ext':
        dst = str(p.with_suffix('.'+new_name))
    elif rule == 'base':
        dst = str(p.with_stem(new_name))
    else:
        dst = str(p) + new_name

    p.rename(dst)
    return dst

if __name__ == '__main__':
    params = {
        "new_name": ".zip",
        "path": ">result[0]",
        "rule": ""
    }
    ctx = {"result": ["v:\\v20250825100235\\六花 喝醉 战斗衔接  锤 击中踩点（邪王真眼） S1 .mp4"]}
    print(main(params, ctx))

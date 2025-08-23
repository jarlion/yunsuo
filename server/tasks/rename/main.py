import os
from pathlib import Path

def main(params:dict, ctx:dict)->dict:
    path = params.get('path')
    new_name = params.get('new_name')
    rule = params.get('rule', '')
    if not path or not new_name:
        return {"error":"Missing required params: path, new_name"}
    try:
        result = rename(path, new_name, rule)
    except Exception as e:
        return {"error":str(e)}
    return {'result': result}

def rename(path:str, new_name:str, rule:str)->str:
    p = Path(path)

    if rule == 'ext':
        dst = str(p.with_suffix('.'+new_name))
    elif rule == 'base':
        dst = str(p.with_stem(new_name))
    else:
        dst = str(p.with_name(new_name))

    os.rename(path, dst)
    return dst

if __name__ == '__main__':
    params = {
        'path': 'test1',
        'new_name': 'zip',
        'rule': 'ext',
    }
    print(main(params, {}))

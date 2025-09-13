import zipfile
from typing import List, Dict, Any
from pathlib import Path
import rarfile
import py7zr

def main(params:Dict[str, Any], ctx:Dict[str, Any]) -> Any|None:
    source_str = params.get('source')
    if not source_str:
        raise ValueError("Missing required params: source")
    password = params.get('password')
    if not password:
        raise ValueError("Missing required params: password")
    type = params.get('type')
    if type not in ['zip', 'rar', '7z']:
        raise ValueError("Invalid params: type")
    source = source_str.strip()
    if source_str.startswith('>'):
        source = eval(source_str[1:], globals(), ctx)
    result = extract(source, password, type)
    if result:
        return [result]
    return None

def extract(source:str, password:str, type:str) -> Path|None:
    source_path = Path(source)
    # 解压zip
    result = try_unzip(source_path, password)
    if result:
        return result
    # 解压rar
    result = try_unrar(source_path, password)
    if result:
        return result
    # 解压7z
    result = try_un7z(source_path, password)
    if result:
        return result
    return None


def try_unzip(path:Path, password:str) -> Path|None:
    try:
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(path.parent, pwd=password.encode() if password else None)
        path = path.parent / path.stem
    except zipfile.BadZipFile as e:
        print(e)
        return None
    return path

def try_unrar(path:Path, password:str) -> Path|None:
    try:
        with rarfile.RarFile(path, 'r') as rar_ref:
            rar_ref.extractall(path.parent, pwd=password)
        path = path.parent / path.stem
    except Exception as e:
        print(e)
        return None
    return path

def try_un7z(path:Path, password:str) -> Path|None:
    try:
        with py7zr.SevenZipFile(path, 'r') as z:
            z.extractall(path.parent, password=password.encode() if password else None)
        path = path.parent / path.stem
    except py7zr.Bad7zFile as e:
        print(e)
        return None
    return path

if __name__ == '__main__':
    def exec_script(script:str, ctx:Dict[str, Any], env:Dict[str, Any]|None=None)->Any:
        if env is None:
            env = globals()
        locals = ctx.copy()
        locals['output'] = None
        exec(script, env, locals)
        return locals.get('output', None)

    result = ["v:\\v20250825100235\\六花 喝醉 战斗衔接  锤 击中踩点（邪王真眼） S1 .mp4"]
    params = {
        "before": "output=cd=result",
        "condition": ">len(cd)",
        "after": "output=cd[:]=cd[1:]"
    }
    dirs = main(params, {"exec_script": exec_script, "result": result})
    print(dirs)
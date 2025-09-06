import os
import re
from typing import List, Dict, Any

def main(params:Dict[str, Any], ctx:Dict[str, Any])->List[Any]:
    script = params.get('script', '')
    if not script:
        raise ValueError("Missing required params: script")
    
    exec_script = ctx.get('exec_script')
    if not exec_script:
        raise ValueError("Missing required ctx: exec_script")
    
    context = ctx.copy()

    result = exec_script(script, context)

    ctx['result'] = result
    return result


if __name__ == '__main__':
    def exec_script(script:str, ctx:Dict[str, Any], env:Dict[str, Any]|None=None)->Any:
        if env is None:
            env = globals()
        locals = ctx.copy()
        locals['output'] = None
        exec(script, env, locals)
        return locals.get('output', None)
    result = 'V:\\M2510-2103\\[Prejudice-Studio] BanG Dream! Ave Mujica 颂乐人偶 - 11 [Bilibili WEB-DL 1080P AVC 8bit AAC MP4][简日内嵌]_3\\[Prejudice-Studio] BanG Dream! Ave Mujica 颂乐人偶 - 11 [Bilibili WEB-DL 1080P AVC 8bit AAC MP4][简日内嵌]_3.mp4'
    dirs = main({'script': '''
if os.path.isfile(result):
    output = result + ".zip"
    print(output)
    '''}, {'exec_script':exec_script, 'result': result})
    print(dirs)


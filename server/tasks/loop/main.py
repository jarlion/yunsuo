from typing import List, Dict, Any

def main(params:Dict[str, Any], ctx:Dict[str, Any]) -> List[Any]|None:
    exec_script =(ctx.get('exec_script'))
    if not exec_script:
        raise ValueError("Missing required ctx: exec_script")
    before_str = params.get('before')
    if not before_str:
        raise ValueError("Missing required params: before")
    condition_str = params.get('condition')
    if not condition_str:
        raise ValueError("Missing required params: condition")
    after_str = params.get('after')
    if not after_str:
        raise ValueError("Missing required params: after")
    call_subtasks = ctx.get('call_subtasks')
    max_count = params.get('max', 1000)

    context = ctx.copy()
    context['cd'] = exec_script(before_str, context)
    result = []
    i = 0
    while eval(condition_str[1:], globals(), context) and i < max_count:
        if call_subtasks:
            context['cur'] = context.get('cd', [])[0]
            result.append(call_subtasks(context))
        exec_script(after_str, context)
        i += 1
    return result

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
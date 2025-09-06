from typing import Callable
from flask import Flask, jsonify
import json
from flask import request
from flask_cors import CORS
import os
import random
from datetime import datetime
import importlib.util
from typing import List,Dict,Any

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'Hello, YunSuo!'

def exec_script(script:str, ctx:Dict[str, Any], env:Dict[str, Any]|None=None)->Any:
    if env is None:
        env = globals()
    locals = ctx.copy()
    locals['output'] = None
    exec(script, env, locals)
    return locals.get('output', None)

def _init_tasks(task_ids: List[str]) -> List[Dict[str, Any]]:
    """
    初始化流水线任务
    :param pl: 流水线
    :return: None
    """
    task_list = app.data.get('tasks')
    tasks = []
    for task_id in task_ids:
        task = find(task_list, lambda t: t.get('id') == task_id)
        if task:
            tasks.append(task)
    return tasks

def _init_context(ctx:Dict[str, Any]):
    """
    初始化上下文
    :param ctx: 上下文
    :return: None
    """
    ctx['app'] = app
    ctx['request'] = request
    ctx['jsonify'] = jsonify
    ctx['json'] = json
    ctx['os'] = os
    ctx['random'] = random
    ctx['datetime'] = datetime
    ctx['importlib'] = importlib
    ctx['exec_script'] = exec_script
    ctx['find'] = find
    ctx['_init_tasks'] = _init_tasks
    return ctx

def _pl_list(name:str|None=None, code:str|None=None, desc:str|None=None, on:bool|None=None):
    """
    获取流水线列表
    :param pl_list: 流水线列表
    :param name: 流水线名称
    :param code: 流水线代码
    :param desc: 流水线描述
    :param on: 是否启用
    :return: 流水线列表
    """
    pl_ls = app.data.get('pl')
    if not pl_ls:
        return []

    if name:
        pl_ls = [pl for pl in pl_ls if name.lower() in pl.get('name', '').lower()]
    if code:
        pl_ls = [pl for pl in pl_ls if code == pl.get('code')]
    if desc:
        pl_ls = [pl for pl in pl_ls if desc.lower() in pl.get('desc', '').lower()]
    if on is not None:
        pl_ls = [pl for pl in pl_ls if pl.get('on') == on]
    # 按照 stars 降序排列
    # 按照 update_time 降序排列 # 负号实现降序
    pl_ls = sorted(pl_ls, key=lambda x: (-x['stars'], -datetime.strptime(x['update_time'], '%Y-%m-%d %H:%M:%S').timestamp()))
    # 根据 tasks 查询 任务
    task_list = app.data.get('tasks')
    result = []
    if task_list:
        for pl in pl_ls:
            new_pl = pl.copy()
            new_pl['tasks'] = _init_tasks(new_pl.get('tasks', []))
            result.append(new_pl)
    return result

@app.route('/pl/list', methods=['POST'])
def pl_list():
    # 读取入参
    req = request.get_json()
    name = req.get('name')
    code = req.get('code')
    desc = req.get('desc')
    on = req.get('on')
   
    try:
        result = _pl_list(name, code, desc, on) 
    except Exception as e:
        return response_error(str(e))

    return response_success(result)

### 流水线增加
@app.route('/pl/add', methods=['POST'])
def pl_add():
    pl_ls = app.data.get('pl')
    try:
        # 新增
        pl = {
            'id': f"PL{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(0, 9999)}",
            'code': '',
            'name': '',
            'ctx': {},
            'desc': '',
            'stars': 0,
            'tasks': [],
            'create_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        pl_ls.append(pl)
    except Exception as e:
        return response_error(str(e))
    return response_success(pl)

@app.route('/pl/copy', methods=['POST'])
def pl_copy():
    req = request.get_json()
    pl_id = req.get('id')
    if not pl_id:
        return response_error('pl_id not be empty')
    try:
        pl_ls = app.data.get('pl')
        pl = find(pl_ls, lambda x: x.get('id') == pl_id)
        if not pl:
            return response_error('pl_id not found')
    except Exception as e:
        return response_error(str(e))
    try:
        pl_ls = app.data.get('pl')
        new_pl = pl.copy()
        new_pl['id'] = f"PL{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(0, 9999)}"
        new_pl['create_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_pl['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_tasks = tasks_copy(new_pl.get('tasks', []))
        # new_pl['tasks_id'] = [t.get('id') for t in new_tasks]
        new_pl['tasks'] = new_tasks
        pl_ls.append(new_pl)
    except Exception as e:
        return response_error(str(e))
    return response_success(new_pl)


### 流水线更新
@app.route('/pl/update', methods=['POST'])
def pl_update():
    # 读取入参
    req = request.get_json()
    id = req.get('id')
    if not id:
        return response_error('id not be empty')
    code = req.get('code')
    name = req.get('name')
    ctx = req.get('ctx',{})
    desc = req.get('desc')
    stars = req.get('stars')
    tasks = req.get('tasks')
    pid = req.get('pid')
    try:
        # 读取json文件
        pl_ls = app.data.get('pl')

        # 查找 id 匹配的项
        pl = find(pl_ls, lambda x: x.get('id') == id)
        if not pl:
            return response_error('id not found')
        if pid:
            pl['pid'] = pid
        if code:
            pl['code'] = code
        if name:
            pl['name'] = name
        if ctx:
            pl['ctx'] = ctx
        if desc:
            pl['desc'] = desc
        if stars:
            pl['stars'] = stars
        if tasks:
            pl['tasks'] = [t.get('id') for t in tasks]
        # 更新时间
        pl['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    except Exception as e:
        return response_error(str(e))
    return response_success(_pl_list())

### 流水线删除
@app.route('/pl/del', methods=['POST'])
def pl_delete():
    ids = request.get_json()
    if not ids:
        return response_error('Missing required params')
    pl_ls = app.data.get('pl')
    if not pl_ls:
        return response_error('pl_ls is empty')
    # 查找并删除指定ids的元素
    pl_ls[:] = [item for item in pl_ls if item.get('id') not in ids]

    _task_del(app.data.get('tasks'), ids)
    
    return response_success(_pl_list(), msg="删除成功")

@app.route('/pl/task/list', methods=['POST'])
def pl_task():
    # 读取入参
    req = request.get_json()
    pl_id = req.get('pl_id')
    if not pl_id:
        return response_error('id not be empty')
    try:
        pl_ls = app.data.get("pl")
        pl = find(pl_ls, lambda p: p.get('id') == pl_id)
        if not pl:
            return response_error('pl not found')
        result = _init_tasks(pl.copy().get('tasks', []))
    except Exception as e:
        return response_error(str(e))
    return response_success(result)


def find(ls:List[Any] ,match:Callable[[Any],bool])->(Any|None):
    """
    查找列表中匹配的项
    :param ls: 列表
    :param match: 匹配函数
    :return: 匹配的项，未找到时返回 None
    """
    for item in ls:
        if match(item):
            return item
    return None

### 流水线运行
@app.route('/pl/exec', methods=['POST'])
def pl_exec():
    # 读取入参
    req = request.get_json()
    id = req.get('id')

    if not id:
        return response_error('id not be empty')
    
    try:
        # 读取json文件
        pl_ls = app.data.get('pl')
        pl = find(pl_ls, lambda p: p.get('id') == id)
        if not pl:
            return response_error('id not found')
        context = _init_context(pl.get('ctx',{}))
        tasks = _init_tasks(pl.get('tasks', []))
        if not tasks:
            return response_error('tasks not found')
        result = exec_tasks(tasks, context)
    except Exception as e:
        return response_error(str(e))
    return response_success(result)

def exec_tasks(tasks:List[dict], ctx: Dict[str, Any]):
    """
    执行任务列表
    :param tasks: 任务列表
    :return: None
    """
    result = None
    for task in tasks:
        if not task.get('on'):
            continue
        code = task.get('code')
        if not code:  # 确保code不为空
            print(f"Warning: Task has no code attribute: {task}")
            continue
        
        call_subtasks = _init_tasks(task.get('children', []))
        if call_subtasks:
            ctx['call_subtasks'] = call_subtasks
        params = init_params(task.get('params', {}), ctx)
        # 先读取info.json获取任务信息
        with open(f'tasks/{code}/def.json', 'r', encoding='utf-8') as f:
            task_info = json.load(f)
            script = task_info.get('script', '')  # 提供默认值
            if not script:  # 确保script不为空
                print(f"Warning: Task {code} has no script attribute")
                continue
                
            # 确保所有参数都是字符串类型
            script_path = os.path.join('tasks', str(code), str(script))
            # 执行脚本
            result = load_and_run(script_path, params=params, ctx=ctx)
            ctx['result'] = result
            # 打印结果
            print(result)
    return result


def init_params(params:Dict[str, str], ctx: Dict[str, Any]):
    """
    初始化参数
    :param params: 参数
    :return: 初始化后的参数
    """
    res = {}
    if not params: 
        return res
    for key, value in params.items():
        if isinstance(value, str) and value.startswith('>'):
            value = eval(value[1:],globals(), ctx)
        res[key] = value
    return res

### 任务定义列表
@app.route('/task/list', methods=['POST'])
def task_list():
    # 读取入参
    req = request.get_json()
    code = req.get('code')
    task_ids = []
    result = []
    try:
        # 如果指定任务编码，返回指定的任务定义，否则返回全部任务定义
        if code:
            if os.path.isdir(os.path.join('tasks', code)):
                # 读取json文件
                with open(os.path.join('tasks', code, 'def.json'), 'r', encoding='utf-8') as f:
                    task = json.load(f)
                    result.append(task)
                    return response_success(result)
        else:
            for dir in os.listdir('tasks'):
                if os.path.isdir(os.path.join('tasks', dir)):
                    # 读取json文件
                    with open(os.path.join('tasks', dir, 'def.json'), 'r', encoding='utf-8') as f:
                        task = json.load(f)
                        result.append(task)

    except Exception as e:
        return response_error(str(e))
    return response_success(result)

### 任务详情
@app.route('/task/detail', methods=['POST'])
def task_detail():
    # 读取入参
    req = request.get_json()
    code = req.get('code')
    try:
        # 读取json文件
        with open('data/task.json', 'r', encoding='utf-8') as f:
            task_list = json.load(f)
            # 如果 code 有值 则根据 code 精确匹配
            if code:
                task_list = [task for task in task_list if task.get('code') == code]
            # 否则返回所有任务
            else:
                task_list = [task for task in task_list]
    except Exception as e:
        return response_error(str(e))
    return response_success(task_list)  

### 任务测试运行
@app.route('/task/test', methods=['POST'])
def task_test():
    # 读取入参
    req = request.get_json()
    code = req.get('code')
    params = req.get('params')
    ctx = _init_context(req.get('ctx',{}))
    try:
        # 读取json文件
        with open(f'tasks/{code}/def.json', 'r', encoding='utf-8') as f:
            task = json.load(f)
            script = task.get('script')
            script_path = os.path.join('tasks', code, script)
            # 执行脚本
            print(isinstance(ctx, dict), ctx.get('root'))
            result = load_and_run(script_path, params=params, ctx=ctx)
    except Exception as e:
        return response_error(str(e))
    return response_success(result)

def tasks_copy(task_ids:List[str]) -> List[Dict[str, Any]]:
    """
    复制任务
    :param task_ids: 任务id列表
    :return: 复制后的任务列表
    """
    task_list = app.data.get('tasks', [])
    new_task_list = []
    task_id_ref:Dict[str, Any] = {}
    for task_id in task_ids:
        task = find(task_list, lambda t: t.get('id') == task_id)
        if not task:
            continue
        new_task = task_copy(task)
        task_id_ref[task_id] = new_task.get('id')
        task_list.append(new_task)
        new_task_list.append(new_task)
    # 处理子任务
    for task in new_task_list:
        parent_id = task.get('pid')
        if parent_id and parent_id in task_id_ref:
            task['pid'] = task_id_ref[parent_id]
    return new_task_list

def task_copy(task:Dict[str, Any]) -> Dict[str, Any]:
    """
    复制任务
    :param task_ids: 任务id列表
    :return: 复制后的任务列表
    """
    new_task = task.copy()
    new_task['id'] = f"T{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(0, 9999)}"        
    new_task['create_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_task['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return new_task

def load_and_run(filepath: str, *args, **kwargs):
    """
    动态加载 filepath 对应的模块并执行其 main(*args, **kwargs)
    返回 main 的返回值
    """
    # 1. 构造模块名（保证唯一，避免缓存冲突）
    mod_name = f"_dyn_{abs(hash(filepath))}"

    # 2. 创建 spec + 模块对象
    spec = importlib.util.spec_from_file_location(mod_name, filepath)
    if not spec:
        raise ImportError(f"Cannot find spec for {filepath}")
    module = importlib.util.module_from_spec(spec)
    if not module:
        raise ImportError(f"Cannot create module for {filepath}")

    # 3. 执行模块代码
    if not spec.loader:
        raise ImportError(f"Cannot find loader for {filepath}")
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        raise ImportError(f"Error executing module {filepath}: {e}")

    # 4. 取 main 函数并调用
    if not hasattr(module, 'main'):
        raise AttributeError(f"{filepath} has no 'main' function")
    try:
        return module.main(*args, **kwargs)
    except Exception as e:
        raise ImportError(f"Error executing module {filepath}: {e}")

### 任务执行  
@app.route('/task/start', methods=['POST'])   
def task_start():
    # 读取入参
    req = request.get_json()
    code = req.get('code')
    if not code:
        return response_error('Missing required params: code')
    try:
        # 读取json文件
        with open(f'tasks/{code}/def.json', 'r', encoding='utf-8') as f:
            task = json.load(f)
            script = task.get('script')
            script_path = os.path.join('tasks', code, script)
            # 执行脚本
            result = load_and_run(script_path, params={'patterns': '[.+]'}, ctx={'root':'./'})
    except Exception as e:
        return response_error(str(e))
    return response_success(result)

def _task_update(new_task:Dict[str, Any], task:Dict[str, Any]):
    """
    更新任务
    :param new_task: 新任务
    :param task: 任务
    :return: 更新后的任务
    """
    new_task['id'] = task.get('id', f"T{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(0, 9999)}")
    new_task['pl_id'] = task.get('pl_id', '')
    new_task['on'] = task.get('on', True)
    new_task['code'] = task.get('code', '')
    new_task['params'] = task.get('params', {})
    new_task['childeren'] = task.get('childeren', [])
    new_task['create_time'] = task.get('create_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    new_task['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return new_task


@app.route('/task/add', methods=['POST'])
def task_add():
    # 读取入参
    req = request.get_json()
    pl_id = req.get('pl_id')
    if not pl_id:
        return response_error('Missing required params: plIid')

    pid = req.get('pid')

    pl = find(app.data.get('pl'), lambda p:p.get('id') == pl_id)
    if not pl:
        return response_error('Plugin not found')
    try:
        tasks_list = app.data.get('tasks')
        new_task = {
            "id": f"T{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(0, 9999)}",
            "pid": pid,
            "pl_id": pl_id,
            "code": "",
            "on": True,
            "params": {},
        }
        tasks_list.append(new_task)

        pl['tasks'].append(new_task.get('id'))
    except Exception as e:
        return response_error(str(e))
    return response_success(new_task)

@app.route('/task/update', methods=['POST'])
def task_update():
    # 读取入参
    task = request.get_json()

    try:
        tasks_list = app.data.get('tasks')
        target_task = find(tasks_list, lambda t:t.get('id') == task.get('id'))
        if not target_task:
            return response_error('Task not found')
        _task_update(target_task, task)
    except Exception as e:
        return response_error(str(e))
    return response_success(target_task, "更新成功")

def _task_del(task_list:List[Dict[str, Any]], ids:List[str]):
    """
    删除任务
    :param task_list: 任务列表
    :param ids: 任务id列表
    :return: 删除后的任务列表
    """
    task_list[:] = [item for item in task_list if item.get('id') not in ids]
    return task_list

@app.route('/task/del', methods=['POST'])
def task_del():
    # 读取入参
    ids = request.get_json()
    if not ids:
        return response_error('Missing required params: ids')

    try:
        tasks_list = app.data.get('tasks')
        _task_del(tasks_list, ids)
        # 删除 pl_list 中每个pl下tasks
        pl_ids = [item.get('pl_id') for item in tasks_list if item.get('id') in ids]
        print(pl_ids)
        pl_ls = app.data.get('pl')
        for pl in pl_ls:
            if pl.get('id') in pl_ids:
                pl['tasks'] = [task_id for task_id in pl['tasks'] if task_id not in ids]
    
    except Exception as e:
        return response_error(str(e))
    # 未定返回结果
    return response_success([], msg="删除成功")


def response_success(data, msg='success', page:dict={}):
    # 请求成功时保存数据
    save_data()
    return jsonify({'code': 'success', 'msg': msg, 'data': data, 'page': page})

def response_error(msg='error', code='error'):
    # 请求失败时不保存数据
    return jsonify({'code': code, 'msg': msg})

@app.route('/all/save', methods=['POST']) 
def all_save():
    # 读取入
    save_data()
    return response_success('success')

# 只在成功响应时保存数据的函数
def save_data():
    # 写入json文件
    pl_ls = app.data.get('pl')
    with open('data/pl.json', 'w', encoding='utf-8') as f:
        json.dump(pl_ls, f, ensure_ascii=False, indent=2)
    tasks_list = app.data.get('tasks')
    with open('data/tasks.json', 'w', encoding='utf-8') as f:
        json.dump(tasks_list, f, ensure_ascii=False, indent=2)

@app.teardown_appcontext
def shutdown_hook(exception = None):
    if exception:
        print(exception)
    # 不再在请求结束时自动保存数据
    # 数据只在response_success中保存
    return

def init_data():
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists('data/pl.json'):
        with open('data/pl.json', 'w', encoding='utf-8') as f:
            pl = json.dump({'pl': []}, f)
    with open('data/pl.json', 'r', encoding='utf-8') as f:
        pl = json.load(f)
    if not os.path.exists('data/tasks.json'):
        with open('data/tasks.json', 'w', encoding='utf-8') as f:
            tasks = json.dump({'tasks': []}, f)
    with open('data/tasks.json', 'r', encoding='utf-8') as f:
        tasks = json.load(f)
    return {"pl": pl, "tasks": tasks}

if __name__ == '__main__':
    app.data= init_data()
    app.run(debug=True, host='0.0.0.0', port=5000)

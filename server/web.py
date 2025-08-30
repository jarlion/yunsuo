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

@app.route('/pl/list', methods=['POST'])
def pl_list():
    # 读取入参
    req = request.get_json()
    name = req.get('name')
    code = req.get('code')
    # ctx = req.get('ctx')
    desc = req.get('desc')
    # tasks = req.get('tasks')
   
    try:
        pl_list = app.data.get('pl')
        # 如果 code 有值 则根据 code 精确匹配
        if code:
            pl_list = [pl for pl in pl_list if pl.get('code') == code]

        # 如果 name 有值 则根据 name 模糊匹配
        if name:
            pl_list = [pl for pl in pl_list if name.lower() in pl.get('name', '').lower()]

        # 如果 desc 有值 则根据 desc 模糊匹配
        if desc:
            pl_list = [pl for pl in pl_list if desc.lower() in pl.get('desc', '').lower()]

        # 按照 stars 降序排列
        pl_list.sort(key=lambda x: x.get('stars', 0), reverse=True)

    except Exception as e:
        return response_error(str(e))

    return response_success(pl_list)

### 流水线增加
@app.route('/pl/add', methods=['POST'])
def pl_add():
    # 读取入参
    req = request.get_json()
    id = f"PL{datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(0, 9999)}"
    code = req.get('code')
    name = req.get('name')
    ctx = req.get('ctx',{})
    desc = req.get('desc')
    stars = req.get('stars')
    tasks = req.get('tasks')

    pl_list = app.data.get('pl')
    try:
        # 新增
        pl = {
            'id': id,
            'code': code,
            'name': name,
            'ctx': ctx,
            'desc': desc,
            'stars': stars,
            'tasks': tasks,
            'create_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        pl_list.append(pl)
    except Exception as e:
        return response_error(str(e))
    return response_success(pl_list)

def find_item_by_id(lst:list, target_id:str)->(dict|None):
    """
    查找列表中 id 匹配的项
    :param lst: 列表
    :param target_id: 目标 id
    :return: 匹配的项，未找到时返回 None
    """
    for item in lst:
        # 检查item是否为字典并包含id键
        if isinstance(item, dict):
            if 'id' in item and item['id'] == target_id:
                return item
        # 检查item是否为对象并包含id属性
        elif hasattr(item, 'id') and item.id == target_id:
            return item
    return None  # 未找到匹配项时返回None

### 流水线更新
@app.route('/pl/update', methods=['POST'])
def pl_update():
    # 读取入参
    req = request.get_json()
    id = req.get('id')
    code = req.get('code')
    name = req.get('name')
    ctx = req.get('ctx',{})
    desc = req.get('desc')
    stars = req.get('stars')
    tasks = req.get('tasks')
    try:
        # 读取json文件
        with open('data/pl.json', 'r', encoding='utf-8') as f:
            pl_list = json.load(f)
            # 如果 id 有值 则根据 id 精确匹配
            if not id:
                return response_error('id not be empty')

            # 查找 id 匹配的项
            pl = find_item_by_id(pl_list, id)
            if not pl:
                return response_error('id not found')
            
            pl['ctx'] = ctx
            pl['code'] = code
            pl['name'] = name
            pl['desc'] = desc
            pl['stars'] = stars
            pl['tasks'] = tasks
            # 更新时间
            pl['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 写入json文件
        with open('data/pl.json', 'w', encoding='utf-8') as f:
            json.dump(pl_list, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return response_error(str(e))
    return response_success(pl_list)

### 流水线删除
@app.route('/pl/del', methods=['POST'])
def pl_delete():
    ids = request.get_json()
    if not ids:
        return response_error('Missing required params')
    pl_list = app.data.get('pl')
    if not pl_list:
        return response_error('pl_list is empty')
    # 查找并删除指定ids的元素
    pl_list[:] = [item for item in pl_list if item.get('id') not in ids]
    
    return response_success(pl_list, msg="删除成功")

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
        with open('data/pl.json', 'r', encoding='utf-8') as f:
            pl_list = json.load(f)
            pl = find(pl_list, lambda x: x.get('id') == id)
            if not pl:
                return response_error('id not found')
            ctx = pl.get('ctx',{})
            tasks = pl.get('tasks')
            if not tasks:
                return response_error('tasks not found')
            result = exec_tasks(tasks, ctx)
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
            value = eval(value[1:])
        res[key] = value
    return res

### 任务列表
@app.route('/task/list', methods=['POST'])
def task_list():
    # 读取入参
    req = request.get_json()
    code = req.get('code')
    result = []
    try:
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
    ctx = req.get('ctx',{})
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
    return module.main(*args, **kwargs)

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


def response_success(data, msg='success', page:dict={}):
    return jsonify({'code': 'success', 'msg': msg, 'data': data, 'page': page})

def response_error(msg='error', code='error'):
    return jsonify({'code': code, 'msg': msg})

@app.teardown_appcontext
def shutdown_hook(exception = None):
    # 写入json文件
    pl_list = app.data.get('pl')
    with open('data/pl.json', 'w', encoding='utf-8') as f:
        json.dump(pl_list, f, ensure_ascii=False, indent=2)
    tasks_list = app.data.get('tasks')
    with open('data/tasks.json', 'w', encoding='utf-8') as f:
        json.dump(tasks_list, f, ensure_ascii=False, indent=2)

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

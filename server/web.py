from flask import Flask, jsonify
import json
from flask import request
from flask_cors import CORS
import os
import importlib.util

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return 'Hello, Flask!'

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
        # 读取json文件
        with open('data/pl.json', 'r', encoding='utf-8') as f:
            pl_list = json.load(f)
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
            if id:
                pl_list = [pl for pl in pl_list if pl.get('id') == id]
                if pl_list:
                    pl = pl_list[0]
                    if ctx:
                        pl['ctx'] = ctx
                    if code:
                        pl['code'] = code
                    if name:
                        pl['name'] = name
                    if desc:
                        pl['desc'] = desc
                    if stars:
                        pl['stars'] = stars
                    if tasks:
                        pl['tasks'] = tasks
            # 否则返回所有任务
            else:
                return response_error('id not found')
        # 写入json文件
        with open('data/pl.json', 'w', encoding='utf-8') as f:
            json.dump(pl_list, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return response_error(str(e))
    return response_success(pl_list)

### 流水线删除
@app.route('/pl/delete', methods=['POST'])
def pl_delete():
    # 读取入参
    ids = request.get_json()
    try:
        # 读取json文件
        with open('data/pl.json', 'r', encoding='utf-8') as f:
            pl_list = json.load(f)
            # 如果 id 有值 则根据 id 精确匹配
            if ids:
                pl_list = [pl for pl in pl_list if pl.get('id') not in ids]
            # 否则返回所有任务
            else:
                return response_error('id not found')
        # 写入json文件
        with open('data/pl.json', 'w', encoding='utf-8') as f:
            json.dump(pl_list, f, ensure_ascii=False, indent=2)
    except Exception as e:
        return response_error(str(e))
    return response_success(pl_list, "delete success")

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
                with open(os.path.join('tasks', dir, 'info.json'), 'r', encoding='utf-8') as f:
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

def load_and_run(filepath: str, *args, **kwargs):
    """
    动态加载 filepath 对应的模块并执行其 main(*args, **kwargs)
    返回 main 的返回值
    """
    # 1. 构造模块名（保证唯一，避免缓存冲突）
    mod_name = f"_dyn_{abs(hash(filepath))}"

    # 2. 创建 spec + 模块对象
    spec   = importlib.util.spec_from_file_location(mod_name, filepath)
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
        with open(f'tasks/{code}/info.json', 'r', encoding='utf-8') as f:
            task = json.load(f)
            script = task.get('script')
            script_path = os.path.join('tasks', code, script)
            # 执行脚本
            result = load_and_run(script_path, params={'patterns': '[.+]'}, ctx={'root':'./'})
    except Exception as e:
        return response_error(str(e))
    return response_success(result)


@app.route('/pl/del')
def pl_del():
    return 'pl_del'

def response_success(data, msg='success', page:dict={}):
    return jsonify({'code': 'success', 'msg': msg, 'data': data, 'page': page})

def response_error(msg='error', code='error'):
    return jsonify({'code': code, 'msg': msg})



class Pipe:
    def __init__(self, links:dict):
        self.links = links
    
    def transform(self, data:dict):
        result = {}
        for link in self.links:
            result[self.links[link]] = data[link]
        return result




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

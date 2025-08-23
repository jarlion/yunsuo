from flask import Flask, jsonify
import json
from flask import request
from flask_cors import CORS
import os

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
    desc = req.get('desc')
    
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

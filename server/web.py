from flask import Flask, jsonify
import json
from flask import request
from flask_cors import CORS
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
        return jsonify({'error': str(e)})

    return jsonify(pl_list)






@app.route('/pl/del')
def pl_del():
    return 'pl_del'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

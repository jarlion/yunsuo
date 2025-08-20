from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import time
import uuid

# 创建FastAPI应用
app = FastAPI(title="Pipeline Server", version="1.0")

# 添加CORS中间件，允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该指定具体的 origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 模拟数据库 - 流水线
pipelines_db: Dict[str, Dict[str, Any]] = {}

# 模拟数据库 - 命令
commands_db: List[Dict[str, Any]] = [
    {
        "id": "1",
        "code": "CMD001",
        "name": "数据清洗",
        "description": "对输入数据进行清洗和预处理",
        "createdAt": "2023-10-01T10:00:00Z"
    },
    {
        "id": "2",
        "code": "CMD002",
        "name": "模型训练",
        "description": "使用训练数据训练模型",
        "createdAt": "2023-10-02T11:30:00Z"
    },
    {
        "id": "3",
        "code": "CMD003",
        "name": "模型评估",
        "description": "评估模型性能指标",
        "createdAt": "2023-10-03T14:15:00Z"
    },
    {
        "id": "4",
        "code": "CMD004",
        "name": "结果导出",
        "description": "导出模型预测结果",
        "createdAt": "2023-10-04T09:45:00Z"
    },
    {
        "id": "5",
        "code": "CMD005",
        "name": "数据可视化",
        "description": "生成数据可视化图表",
        "createdAt": "2023-10-05T16:20:00Z"
    }
]

# 流水线模型
class PipelineModel(BaseModel):
    name: str
    description: Optional[str] = None
    commands: Optional[List[str]] = None  # 命令ID列表

# 更新流水线模型
class UpdatePipelineModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    commands: Optional[List[str]] = None

# 根路由
@app.get("/")
def read_root():
    return {"message": "Pipeline Server is running"}

# 命令列表接口
@app.get("/api/cmd/list")
def get_commands(
    query: Optional[str] = Query(None, description="搜索关键词，匹配code或name"),
    page: int = Query(1, ge=1, description="页码"),
    pageSize: int = Query(10, ge=1, le=100, description="每页数量")
):
    # 搜索功能
    filtered_commands = commands_db
    if query:
        query = query.lower()
        filtered_commands = [
            cmd for cmd in commands_db
            if query in cmd["code"].lower() or query in cmd["name"].lower()
        ]

    # 分页功能
    total = len(filtered_commands)
    start = (page - 1) * pageSize
    end = start + pageSize
    paginated_commands = filtered_commands[start:end]

    return {
        "items": paginated_commands,
        "total": total,
        "page": page,
        "pageSize": pageSize
    }

# 新增流水线接口
@app.post("/api/pl/add")
def add_pipeline(pipeline: PipelineModel):
    pipeline_id = str(uuid.uuid4())[:8]
    new_pipeline = {
        "id": pipeline_id,
        "name": pipeline.name,
        "description": pipeline.description,
        "commands": pipeline.commands or [],
        "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "updatedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    pipelines_db[pipeline_id] = new_pipeline
    return {
        "success": True,
        "message": "流水线添加成功",
        "data": new_pipeline
    }

# 更新流水线接口
@app.put("/api/pl/update/{pipeline_id}")
def update_pipeline(pipeline_id: str, pipeline: UpdatePipelineModel):
    if pipeline_id not in pipelines_db:
        raise HTTPException(status_code=404, detail="流水线不存在")

    existing_pipeline = pipelines_db[pipeline_id]

    # 更新字段
    if pipeline.name is not None:
        existing_pipeline["name"] = pipeline.name
    if pipeline.description is not None:
        existing_pipeline["description"] = pipeline.description
    if pipeline.commands is not None:
        existing_pipeline["commands"] = pipeline.commands

    existing_pipeline["updatedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    pipelines_db[pipeline_id] = existing_pipeline

    return {
        "success": True,
        "message": "流水线更新成功",
        "data": existing_pipeline
    }

# 运行流水线接口
@app.post("/api/pl/run/{pipeline_id}")
def run_pipeline(pipeline_id: str):
    if pipeline_id not in pipelines_db:
        raise HTTPException(status_code=404, detail="流水线不存在")

    pipeline = pipelines_db[pipeline_id]

    # 模拟流水线运行
    # 在实际应用中，这里应该触发真实的流水线执行逻辑
    pipeline["lastRunAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    pipeline["status"] = "running"
    pipelines_db[pipeline_id] = pipeline

    return {
        "success": True,
        "message": "流水线已开始运行",
        "data": pipeline
    }

# 查询流水线接口
@app.get("/api/pl/list")
def get_pipelines(
    query: Optional[str] = Query(None, description="搜索关键词，匹配name"),
    page: int = Query(1, ge=1, description="页码"),
    pageSize: int = Query(10, ge=1, le=100, description="每页数量")
):
    # 搜索功能
    filtered_pipelines = list(pipelines_db.values())
    if query:
        query = query.lower()
        filtered_pipelines = [
            pl for pl in filtered_pipelines
            if query in pl["name"].lower()
        ]

    # 分页功能
    total = len(filtered_pipelines)
    start = (page - 1) * pageSize
    end = start + pageSize
    paginated_pipelines = filtered_pipelines[start:end]

    return {
        "items": paginated_pipelines,
        "total": total,
        "page": page,
        "pageSize": pageSize
    }

# 删除流水线接口
@app.delete("/api/pl/del/{pipeline_id}")
def delete_pipeline(pipeline_id: str):
    if pipeline_id not in pipelines_db:
        raise HTTPException(status_code=404, detail="流水线不存在")

    deleted_pipeline = pipelines_db.pop(pipeline_id)

    return {
        "success": True,
        "message": "流水线删除成功",
        "data": deleted_pipeline
    }

# 运行服务器的入口点
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
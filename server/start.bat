@echo off

REM 检查Rust编译器是否已安装
rustc --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 警告: 未检测到Rust编译器。安装pydantic-core需要Rust编译器。
    echo 请先安装Rust编译器: https://www.rust-lang.org/tools/install
    pause
    exit /b 1
)

REM 创建虚拟环境（如果不存在）
if not exist venv (
    echo 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 安装依赖
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo 依赖安装失败。请确保已安装Rust编译器并尝试再次运行此脚本。
    pause
    exit /b 1
)

REM 启动服务
echo 启动服务端...
python web.py

pause
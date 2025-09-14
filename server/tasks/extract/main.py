#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import shutil
from pathlib import Path
from typing import Dict, Any
import subprocess

# ---------- 通用解压 ----------
def main(params: Dict[str, Any], ctx: Dict[str, Any]) -> str:
    source = params["source"]
    password = params.get("password", "")
    remove = params.get("remove", False)
    try:
        src = eval(source[1:], globals(), ctx) if source.startswith(">") else source
    except Exception as e:
        print(f"[extract] source表达式求值失败: {e}")
        raise e
    try:
        result = unrar_with_winrar(src, password)
    except Exception as e:
        print(f"[extract] 解压失败: {e}")
        raise e
    if remove:
        source_path = Path(src)
        if source_path.is_dir():
            shutil.rmtree(source_path)
        elif source_path.is_file():
            source_path.unlink()
    return str(result)

def unrar_with_winrar(source: str, password: str = "") -> Path:
    """
    解压 RAR -> 源文件同级 / 去后缀文件夹
    返回解压目录 Path
    """
    src = Path(source).resolve()
    if not src.exists() :
        raise FileNotFoundError("源文件不存在或后缀错误")
    # 解压前判断磁盘空间够不够
    if src.stat().st_size > shutil.disk_usage(src).free:
        raise RuntimeError("磁盘空间不足")

    # 输出目录 = 同级 / 源文件名（去后缀）
    out_dir = src.with_suffix("")
    out_dir.mkdir(exist_ok=True)

    # WinRAR 路径（若不在 PATH 则填写完整路径）
    winrar_exe = shutil.which("WinRAR.exe") or shutil.which("rar.exe") or r"D:\Program Files\WinRAR\WinRAR.exe"

    # 构造命令行
    cmd = [
        winrar_exe,
        "x",                     # 解压模式
        "-y",                    # 自动覆盖
        "-p" + password,         # 密码（空字符串时 -p 后面无内容）
        str(src),                # 源文件
        str(out_dir) + "\\",     # 目标目录（WinRAR 要求以 \ 结尾）
    ]

    # 执行
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"WinRAR 解压失败: {e.stderr}") from e

    return out_dir

# ---------- 本地测试 ----------
if __name__ == '__main__':
    params = {
        "source": r"V:\yhsn_hidden_8.zip",
        "password": "图图有佳人",
        "remove": True,
    }
    result = main(params, {})
    print("最终解压目录:", result)

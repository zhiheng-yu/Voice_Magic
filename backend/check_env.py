import sys
import os

print("=" * 60)
print("元视界AI妙妙屋—声音魔法 - 后端环境检查")
print("=" * 60)
print()

print("Python版本:", sys.version)
print()

missing_packages = []

try:
    import fastapi
    print("✓ fastapi 已安装")
except ImportError:
    print("✗ fastapi 未安装")
    missing_packages.append("fastapi")

try:
    import uvicorn
    print("✓ uvicorn 已安装")
except ImportError:
    print("✗ uvicorn 未安装")
    missing_packages.append("uvicorn")

try:
    import dashscope
    print("✓ dashscope 已安装")
except ImportError:
    print("✗ dashscope 未安装")
    missing_packages.append("dashscope")

try:
    import requests
    print("✓ requests 已安装")
except ImportError:
    print("✗ requests 未安装")
    missing_packages.append("requests")

try:
    import dotenv
    print("✓ python-dotenv 已安装")
except ImportError:
    print("✗ python-dotenv 未安装")
    missing_packages.append("python-dotenv")

print()

if missing_packages:
    print("缺少以下依赖包:")
    for pkg in missing_packages:
        print(f"  - {pkg}")
    print()
    print("请运行以下命令安装:")
    print(f"pip install {' '.join(missing_packages)}")
    sys.exit(1)
else:
    print("✓ 所有依赖包已安装")
    print()

print("检查环境变量...")
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("DASHSCOPE_API_KEY")
if api_key:
    print("✓ DASHSCOPE_API_KEY 已配置")
else:
    print("✗ DASHSCOPE_API_KEY 未配置")
    print("  请在 backend/.env 文件中配置 API Key")

region = os.getenv("REGION", "beijing")
print(f"✓ REGION: {region}")

print()
print("=" * 60)
print("环境检查完成！")
print("=" * 60)

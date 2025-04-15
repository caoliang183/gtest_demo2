import os
import subprocess
import requests
import sys

# 设置标准输出的编码为 UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# 检查环境变量 FEISHU_WEBHOOK 是否存在
feishu_webhook = os.getenv('FEISHU_WEBHOOK')
if not feishu_webhook:
    print("Missing FEISHU_WEBHOOK")
    exit(1)

# 检查测试状态
status = "✅ 所有测试通过"
try:
    result = subprocess.run(['grep', '-r', '<Failure>', 'build/Testing'], capture_output=True, text=True)
    if result.returncode == 0:
        status = "❌ 测试失败"
except FileNotFoundError:
    print("grep 命令未找到，请确保已安装。")
    exit(1)

# 构建飞书消息内容
github_server_url = os.getenv('GITHUB_SERVER_URL')
github_repository = os.getenv('GITHUB_REPOSITORY')
github_run_id = os.getenv('GITHUB_RUN_ID')
message = f"GTest 测试完成\n状态：{status}\n详情：{github_server_url}/{github_repository}/actions/runs/{github_run_id}"

# 发送 POST 请求到飞书 Webhook
headers = {'Content-Type': 'application/json'}
data = {
    "msg_type": "text",
    "content": {
        "text": message
    }
}
try:
    response = requests.post(feishu_webhook, json=data, headers=headers)
    response.raise_for_status()
except requests.RequestException as e:
    print(f"发送请求到飞书 Webhook 时出错: {e}")
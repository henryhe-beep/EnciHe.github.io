# ...existing code...
from datetime import datetime
import json
import os

# 不再调用 scholarly；优先使用本地缓存，否则写入占位数据（避免任何 Google Scholar 网络请求）
os.makedirs('results', exist_ok=True)
cache_file = 'results/gs_data.json'

author = None
if os.path.exists(cache_file):
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            author = json.load(f)
    except Exception:
        author = None

if not author:
    # 使用环境变量作为可读名称的来源（可为空），但不进行任何外部请求
    author = {
        "name": os.environ.get('GOOGLE_SCHOLAR_ID', 'Unknown'),
        "citedby": 0,
        "updated": str(datetime.now()),
        "publications": {}
    }

# 写入缓存与 shields.io 文件
with open(cache_file, 'w', encoding='utf-8') as outfile:
    json.dump(author, outfile, ensure_ascii=False, indent=2)

shieldio_data = {
  "schemaVersion": 1,
  "label": "citations",
  "message": f"{author.get('citedby', 0)}",
}
with open('results/gs_data_shieldsio.json', 'w', encoding='utf-8') as outfile:
    json.dump(shieldio_data, outfile, ensure_ascii=False, indent=2)

print(json.dumps(author, ensure_ascii=False, indent=2))
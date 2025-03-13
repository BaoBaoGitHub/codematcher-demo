"""
把pkl数据变为jsonl数据
"""

import os
import pickle
import json

# 定义输入和输出路径
input_dir = "/home/baoxuanlin/code/codematcher-demo/unzipdata"
output_dir = "/home/baoxuanlin/code/codematcher-demo/jsonl_output"

# 创建输出目录（如果不存在）
os.makedirs(output_dir, exist_ok=True)

# 遍历范围 0 到 165 的 pkl 文件
pkl_files = [f"data{i}.pkl" for i in range(166)]

for pkl_file in pkl_files:
    # 生成完整路径
    pkl_path = os.path.join(input_dir, pkl_file)
    jsonl_path = os.path.join(output_dir, pkl_file.replace(".pkl", ".jsonl"))

    # 检查文件是否存在
    if not os.path.exists(pkl_path):
        print(f"文件不存在，跳过: {pkl_path}")
        continue

    # 读取 pkl 文件
    with open(pkl_path, "rb") as f:
        data = pickle.load(f)

        # 检查是否是列表类型
        if not isinstance(data, list):
            print(f"{pkl_file} 中的数据不是列表，跳过")
            continue

        # 写入到对应的 jsonl 文件
        with open(jsonl_path, "w") as jsonl_file:
            for item in data:
                # 格式化为指定格式
                json_item = {
                    "_index": "search_engine",
                    "_source": item["_source"],
                    "content": item["_source"]["source"]
                }
                # 写入 jsonl 文件
                jsonl_file.write(json.dumps(json_item) + "\n")

    print(f"已将 {pkl_file} 转换为 {jsonl_path}")

print(f"所有文件转换完成，输出目录为: {output_dir}")

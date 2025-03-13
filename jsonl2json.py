"""把jsonl文件转变为json文件"""

import os
import json

# 输入和输出目录
input_dir = "/home/baoxuanlin/code/codematcher-demo/jsonl_output"
output_dir = "/home/baoxuanlin/code/codematcher-demo/json_output"

# 创建输出目录（如果不存在）
os.makedirs(output_dir, exist_ok=True)

# 遍历 data0.jsonl 到 data165.jsonl
for i in range(166):
    input_file = os.path.join(input_dir, f"data{i}.jsonl")
    output_file = os.path.join(output_dir, f"data{i}.json")

    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"文件不存在，跳过: {input_file}")
        continue

    # 转换为 JSON 格式
    data_list = []
    with open(input_file, "r") as f_in:
        for line in f_in:
            # 解析 JSONL 每一行
            data_list.append(json.loads(line))

    # 保存为 JSON 文件
    with open(output_file, "w") as f_out:
        json.dump(data_list, f_out, indent=4)

    print(f"已将 {input_file} 转换为 {output_file}")

print("所有文件转换完成！")

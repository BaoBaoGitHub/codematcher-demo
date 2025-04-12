import json

# 第一步：读取 search_results_32.jsonl 并构建字典
search_dict = {}
with open('/home/baoxuanlin/code/codematcher-demo/search_results_32.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        name = obj['name']
        search_dict[name] = obj

# 第二步：读取 humaneval-java.jsonl 并与 search_dict 中的对象合并，写入结果文件
with open('/home/baoxuanlin/code/codematcher-demo/humaneval-java.jsonl', 'r', encoding='utf-8') as f_in, \
     open('/home/baoxuanlin/code/codematcher-demo/humaneval-java-merge_search_results.jsonl', 'w', encoding='utf-8') as f_out:
    for line in f_in:
        humaneval_obj = json.loads(line)
        name = humaneval_obj['name']
        search_obj = search_dict[name]  # 根据 name 查找对应的对象
        # 合并两个对象，search_obj 的字段会覆盖 humaneval_obj 中除 name 外的同名字段（若有）
        merged_obj = {**humaneval_obj, **search_obj}
        # 将合并后的对象写入输出文件，每行一个 JSON 对象
        f_out.write(json.dumps(merged_obj) + '\n')
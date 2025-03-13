import json
import re

def extract_description_from_jsonl(file_path):
    """
    从JSONL文件中提取“prompt”字段中类定义内部、静态方法之前以“//”开头的注释中的说明部分，
    并记录对应的“name”字段。

    参数：
        file_path (str): JSONL文件路径

    返回：
        list: 包含字典的列表，每个字典包含“name”和“description”
    """
    results = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 解析每行的JSON对象
            data = json.loads(line.strip())
            name = data.get('name', 'Unknown')  # 获取“name”字段，默认为'Unknown'
            prompt = data.get('prompt', '')     # 获取“prompt”字段

            # 定义正则表达式，匹配class和public static之间的内容
            pattern = r'(?<=class\s+\w+\s*{).*?(?=public\s+static)'
            match = re.search(pattern, prompt, re.DOTALL)

            if match:
                # 提取匹配到的注释部分
                comments_section = match.group(0)
                # 匹配以“//”开头的行
                comment_lines = re.findall(r'^\s*//.*$', comments_section, re.MULTILINE)

                # 提取说明部分
                description = []
                for comment in comment_lines:
                    # 去除“//”和前后空白
                    cleaned_comment = comment.strip().lstrip('//').strip()
                    # 如果行中包含“>>>”或“(”，则停止提取
                    if '>>>' in cleaned_comment or '(' in cleaned_comment:
                        break
                    description.append(cleaned_comment)

                # 如果提取到说明部分，记录“name”和“description”
                if description:
                    results.append({
                        'name': name,
                        'description': ' '.join(description)
                    })

    return results

# 示例使用
if __name__ == "__main__":
    # 假设JSONL文件路径为'example.jsonl'
    file_path = '/home/baoxuanlin/code/codematcher-demo/humaneval-java.jsonl'
    try:
        results = extract_description_from_jsonl(file_path)
        print("提取的说明内容：")
        # for item in results:
        #     print(f"Name: {item['name']}")
        #     print(f"Description: {item['description']}")
        #     print("-" * 20)

        # 构造新文件的路径
        new_file_path = file_path.rsplit('/', 1)[0] + '/parsed_question.jsonl'
        
        # 将结果写入新文件
        with open(new_file_path, 'w', encoding='utf-8') as new_file:
            for item in results:
                json.dump(item, new_file, ensure_ascii=False)
                new_file.write('\n')  # 每个结果后换行，以符合JSONL格式
                
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到，请检查路径。")
    except json.JSONDecodeError:
        print("JSON解析错误，请检查文件格式。")
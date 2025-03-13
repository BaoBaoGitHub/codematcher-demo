import pickle
import os

def read_pkl(file_path):
    """
    读取并打印 .pkl 文件的内容
    """
    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在！")
        return

    with open(file_path, 'rb') as file:
        data = pickle.load(file)
        print(f"读取 {file_path} 文件内容：\n")
        
        # 判断内容类型并格式化输出
        if isinstance(data, list):
            print(f"列表长度: {len(data)}")
            # return data
            # for i, item in enumerate(data[:10]):  # 仅打印前 5 条
            #     print(f"第 {i + 1} 条内容:\n{item}\n")
        elif isinstance(data, dict):
            print("字典内容：")
            for key, value in data.items():
                print(f"{key}: {value}\n")
        else:
            print("其他类型数据：")
            print(data)

# 示例调用
if __name__ == "__main__":
    for i in range(165):
        file_path = f"/home/baoxuanlin/code/codematcher-demo/unzipdata/data{i}.pkl"  # 修改为您需要检查的 .pkl 文件路径
        read_pkl(file_path)

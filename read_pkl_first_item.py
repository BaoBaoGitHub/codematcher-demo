import pickle
import os

def check_pkl(file_path):
    """
    查看 .pkl 文件类型，并打印第一条数据
    """
    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在！")
        return

    with open(file_path, 'rb') as file:
        data = pickle.load(file)

        print(f"文件 {file_path} 加载成功！")
        print(f"数据类型：{type(data)}")

        # 输出第一条数据
        if isinstance(data, list) and data:
            print(f"列表的第一条数据：\n{data[0]}")
        elif isinstance(data, dict):
            print("字典的第一条键值对：")
            for key, value in data.items():
                print(f"{key}: {value}")
                break
        else:
            print("无法识别的数据类型或数据为空。")

# 示例调用
if __name__ == "__main__":
    file_path = "unzipdata/data0.pkl"  # 修改为您要检查的 .pkl 文件路径
    check_pkl(file_path)

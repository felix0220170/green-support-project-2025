import json
import math
import os

def count_and_split_json(input_file, keys_per_file=50):
    """
    统计JSON文件的key数量并按指定数量切分成多个txt文件
    :param input_file: 输入的JSON文件路径
    :param keys_per_file: 每个输出文件包含的key数量
    """
    # 读取JSON文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 统计key数量
    total_keys = len(data.keys())
    print(f"JSON文件中共有 {total_keys} 个key")
    
    # 计算需要生成的文件数量
    num_files = math.ceil(total_keys / keys_per_file)
    print(f"将切分成 {num_files} 个文件，每个文件包含 {keys_per_file} 个key")
    
    # 提取所有key并排序
    sorted_keys = sorted(data.keys())
    
    # 切分并生成文件
    for i in range(num_files):
        # 计算当前文件包含的key范围
        start_idx = i * keys_per_file
        end_idx = min((i + 1) * keys_per_file, total_keys)
        
        # 提取当前文件的key和对应的值
        current_data = {}
        for key in sorted_keys[start_idx:end_idx]:
            current_data[key] = data[key]
        
        # 生成文件名和路径
        output_file = f"output/green_finance_part_{i+1}.txt"
        
        # 确保output目录存在
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(current_data, f, ensure_ascii=False, indent=2)
        
        print(f"已生成文件: {output_file}, 包含 {end_idx - start_idx} 个key")


if __name__ == "__main__":
    # 默认每个文件包含50个key，可以根据需要修改
    count_and_split_json('output/green_finance_2025.json', keys_per_file=50)

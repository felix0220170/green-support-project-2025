import json
import os

# 定义文件路径
INPUT_FILE = 'output/two_level_structure.json'
OUTPUT_FILE = 'output/modified_two_level_structure.json'

def modify_two_level_data():
    """
    修改两层结构数据：
    1. 去掉所有元素的row_num属性
    2. 将F列值转换为数字代码（1表示√，2表示√√）
    3. 将B列值转换为4位字符串格式并保留前导零
    """
    # 读取原始数据
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 处理数据
    for parent in data:
        # 处理子元素
        for child in parent['children']:
            # 1. 去掉row_num属性
            if 'row_num' in child:
                del child['row_num']
            
            # 2. 将F列值转换为数字代码
            if 'F' in child:
                f_value = child['F']
                if f_value == '√':
                    child['F'] = 1
                elif f_value == '√√':
                    child['F'] = 2
                else:
                    child['F'] = 0  # 默认值
            
            # 3. 将B列值转换为4位字符串格式并保留前导零，同时保留"-"值
            if 'B' in child:
                b_value = child['B']
                # 转换为字符串
                if b_value is None:
                    # 如果是None，设置为默认值"0000"
                    child['B'] = "0000"
                elif isinstance(b_value, str):
                    # 如果是字符串，先去除可能的空格
                    b_value = b_value.strip()
                    if b_value == "-":
                        # 保留"-"值
                        child['B'] = "-"
                    else:
                        # 尝试转换为数字
                        try:
                            int_value = int(b_value)
                            child['B'] = f"{int_value:04d}"
                        except ValueError:
                            # 如果无法转换为数字且不是"-", 设置为默认值
                            child['B'] = "0000"
                elif isinstance(b_value, int):
                    child['B'] = f"{b_value:04d}"
                else:
                    # 其他类型，设置为默认值
                    child['B'] = "0000"
            else:
                # 如果没有B列，添加默认值
                child['B'] = "0000"
    
    # 保存修改后的数据
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"修改完成！")
    print(f"修改后的数据已保存到: {OUTPUT_FILE}")
    
    # 统计信息
    total_children = sum(len(parent['children']) for parent in data)
    print(f"\n数据统计:")
    print(f"  父元素数量: {len(data)}")
    print(f"  子元素总数量: {total_children}")

if __name__ == "__main__":
    modify_two_level_data()

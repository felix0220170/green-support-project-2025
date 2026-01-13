import json
import os
import re

# 定义文件路径
INPUT_FILE = 'output/cleaned_two_level_structure.json'
OUTPUT_FILE = 'output/final_two_level_structure.json'

def remove_category_id_from_name():
    """
    从所有父元素的category_name中去掉category_id的部分
    例如：将"1.1.1 节能锅炉制造"修改为"节能锅炉制造"
    """
    # 读取原始数据
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 处理数据
    for parent in data:
        category_id = parent['category_id']
        category_name = parent['category_name']
        
        # 使用正则表达式去掉category_id部分
        # 匹配category_id后跟一个空格的模式
        new_name = re.sub(r'^' + re.escape(category_id) + r'\s*', '', category_name)
        
        # 更新category_name
        parent['category_name'] = new_name
    
    # 保存修改后的数据
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"修改完成！")
    print(f"修改后的数据已保存到: {OUTPUT_FILE}")
    
    # 统计信息和示例
    print(f"\n数据统计:")
    print(f"  父元素数量: {len(data)}")
    print(f"  子元素总数量: {sum(len(parent['children']) for parent in data)}")
    
    # 打印前几个父元素的修改示例
    print(f"\n修改示例（前5个父元素）:")
    for i, parent in enumerate(data[:5]):
        print(f"  {i+1}. category_id: {parent['category_id']}")
        print(f"     category_name: {parent['category_name']}")

if __name__ == "__main__":
    remove_category_id_from_name()

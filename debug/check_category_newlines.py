import json
import re

# 读取最终的两层结构数据
final_file_path = '../src/output/final_two_level_structure.json'
with open(final_file_path, 'r', encoding='utf-8') as f:
    final_data = json.load(f)

print("检查category_name中的换行符或特殊字符：")

# 检查所有category_name
for i, parent in enumerate(final_data):
    category_id = parent['category_id']
    category_name = parent['category_name']
    
    # 检查是否包含换行符或其他特殊字符
    if '\n' in category_name:
        print(f"\n找到包含换行符的category_name：")
        print(f"  序号: {i+1}")
        print(f"  category_id: {category_id}")
        print(f"  category_name: {repr(category_name)}")
        print(f"  字符数: {len(category_name)}")
    elif '\r' in category_name:
        print(f"\n找到包含回车符的category_name：")
        print(f"  序号: {i+1}")
        print(f"  category_id: {category_id}")
        print(f"  category_name: {repr(category_name)}")
    elif any(c < ' ' for c in category_name):
        print(f"\n找到包含控制字符的category_name：")
        print(f"  序号: {i+1}")
        print(f"  category_id: {category_id}")
        print(f"  category_name: {repr(category_name)}")

# 使用正则表达式查找所有可能的空白字符
print("\n使用正则表达式查找所有可能的空白字符：")
for i, parent in enumerate(final_data):
    category_id = parent['category_id']
    category_name = parent['category_name']
    
    # 查找所有空白字符
    whitespace_chars = re.findall(r'\s', category_name)
    if whitespace_chars:
        # 获取不同类型的空白字符
        unique_whitespace = set(whitespace_chars)
        print(f"\n找到包含空白字符的category_name：")
        print(f"  序号: {i+1}")
        print(f"  category_id: {category_id}")
        print(f"  category_name: {repr(category_name)}")
        print(f"  空白字符类型: {[repr(c) for c in unique_whitespace]}")

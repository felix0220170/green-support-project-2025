import json
import re

# 读取清理后的两层结构数据
cleaned_file_path = '../src/output/final_two_level_structure_cleaned.json'
with open(cleaned_file_path, 'r', encoding='utf-8') as f:
    cleaned_data = json.load(f)

# 读取原始数据进行对比
original_file_path = '../src/output/final_two_level_structure.json'
with open(original_file_path, 'r', encoding='utf-8') as f:
    original_data = json.load(f)

print("验证清理后的category_name：")

# 1. 检查是否还有包含问题的category_name
print("\n1. 检查是否还有包含问题的category_name：")
problem_count = 0
for parent in cleaned_data:
    category_name = parent['category_name']
    
    if '\n' in category_name:
        print(f"   ❌ 发现包含换行符的category_name：{repr(category_name)}")
        problem_count += 1
    elif re.search(r'([\u4e00-\u9fa5])\s+([\u4e00-\u9fa5])', category_name):
        print(f"   ❌ 发现包含中文字符间空格的category_name：{repr(category_name)}")
        problem_count += 1

if problem_count == 0:
    print(f"   ✅ 所有category_name都已清理干净")

# 2. 显示修改前后的对比
print("\n2. 修改前后的对比：")
modified_count = 0
for orig_parent, cleaned_parent in zip(original_data, cleaned_data):
    orig_name = orig_parent['category_name']
    cleaned_name = cleaned_parent['category_name']
    
    if orig_name != cleaned_name:
        modified_count += 1
        print(f"   {modified_count}. category_id: {orig_parent['category_id']}")
        print(f"      原始名称: {repr(orig_name)}")
        print(f"      清理后: {repr(cleaned_name)}")

# 3. 检查特定的修改示例
print("\n3. 检查特定的修改示例：")
# 检查之前发现的包含空格的category_name
check_ids = ['1.1.9', '2.1.8', '2.3.3', '6.2.9']
for parent in cleaned_data:
    if parent['category_id'] in check_ids:
        print(f"   category_id: {parent['category_id']}")
        print(f"   category_name: {repr(parent['category_name'])}")

# 4. 数据统计
print("\n4. 数据统计：")
print(f"   父元素数量: {len(cleaned_data)}")
print(f"   子元素总数量: {sum(len(parent['children']) for parent in cleaned_data)}")
print(f"   处理的category_name数量: {modified_count}")

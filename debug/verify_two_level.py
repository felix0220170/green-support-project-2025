import json

# 读取两层结构的数据
file_path = '../src/output/two_level_structure.json'
with open(file_path, 'r', encoding='utf-8') as f:
    two_level_data = json.load(f)

print(f"共处理了 {len(two_level_data)} 个父元素")

# 查找包含"余热余压余气利用"的父元素
print("\n查找包含'余热余压余气利用'的父元素：")
found = False
for parent in two_level_data:
    if '余热余压余气利用' in parent['category_name']:
        print(f"✅ 找到父元素：")
        print(f"   category_id: {parent['category_id']}")
        print(f"   category_name: {parent['category_name']}")
        print(f"   子元素数量: {len(parent['children'])}")
        
        # 查看子元素
        print(f"\n   子元素详情：")
        for i, child in enumerate(parent['children']):
            print(f"     子元素 {i+1}：")
            print(f"       B: {child['B']}")
            print(f"       C: {child['C']}")
            print(f"       D: {child['D'][:50]}..." if child['D'] and isinstance(child['D'], str) and len(child['D']) > 50 else f"       D: {child['D']}")
            print(f"       E: {child['E']}")
            print(f"       F: {child['F']}")
            print(f"       row_num: {child['row_num']}")
        found = True
        break

if not found:
    print("❌ 未找到包含'余热余压余气利用'的父元素")

# 查看前10个父元素，检查是否有重复
print("\n\n前10个父元素：")
for i, parent in enumerate(two_level_data[:10]):
    print(f"  {i+1}. {parent['category_name']} (子元素数量: {len(parent['children'])})")

# 检查是否有重复的category_id
print("\n检查是否有重复的category_id：")
category_ids = []
duplicate_ids = []
for parent in two_level_data:
    if parent['category_id'] in category_ids:
        if parent['category_id'] not in duplicate_ids:
            duplicate_ids.append(parent['category_id'])
    else:
        category_ids.append(parent['category_id'])

if duplicate_ids:
    print(f"❌ 发现重复的category_id: {duplicate_ids}")
else:
    print("✅ 所有category_id都是唯一的")
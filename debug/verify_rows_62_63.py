import json

# 读取两层结构的数据
file_path = '../src/output/two_level_structure.json'
with open(file_path, 'r', encoding='utf-8') as f:
    two_level_data = json.load(f)

# 查找1.1.17父元素
print("查找1.1.17父元素：")
for parent in two_level_data:
    if parent['category_id'] == '1.1.17':
        print(f"找到父元素：")
        print(f"  category_id: {parent['category_id']}")
        print(f"  category_name: {parent['category_name']}")
        print(f"  子元素数量: {len(parent['children'])}")
        
        # 打印所有子元素的row_num
        print("\n  子元素的row_num：")
        row_nums = []
        for i, child in enumerate(parent['children']):
            print(f"    子元素 {i+1}: row_num = {child['row_num']}")
            row_nums.append(child['row_num'])
        
        # 检查是否包含行62和行63
        if 62 in row_nums and 63 in row_nums:
            print("\n  ✅ 包含行62和行63")
        else:
            print("\n  ❌ 不包含行62和行63")
            print(f"     缺失的行: {[62, 63] if 62 not in row_nums and 63 not in row_nums else [62] if 62 not in row_nums else [63]}")
        
        break

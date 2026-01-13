import json

# 读取两层结构数据
file_path = '../src/output/two_level_structure.json'
with open(file_path, 'r', encoding='utf-8') as f:
    two_level_data = json.load(f)

# 查找B=3411的子元素
print("查找B=3411的子元素：")
found = False
for parent in two_level_data:
    for child in parent['children']:
        if child['B'] == 3411:
            found = True
            print(f"\n✅ 找到子元素：")
            print(f"  父元素: {parent['category_name']}")
            print(f"  B: {child['B']}")
            print(f"  D列开头: {child['D'][:100]}..." if isinstance(child['D'], str) else f"  D: {child['D']}")
            
            # 检查D列是否包含错误的前缀
            if '1.1 高效节能装备制造' in child['D']:
                print("  ❌ D列仍然包含错误的前缀 '1.1 高效节能装备制造'")
            elif '条件/标准' in child['D']:
                print("  ❌ D列仍然包含错误的前缀 '条件/标准'")
            else:
                print("  ✅ D列不再包含错误的前缀")
            
            break
    if found:
        break

if not found:
    print("❌ 未找到B=3411的子元素")

# 检查之前发现的1.1.17父元素是否仍然正确
print("\n\n检查1.1.17父元素：")
for parent in two_level_data:
    if parent['category_id'] == '1.1.17':
        print(f"✅ 找到1.1.17父元素：")
        print(f"  category_name: {parent['category_name']}")
        print(f"  子元素数量: {len(parent['children'])}")
        
        # 检查子元素是否包含行62和行63
        row_nums = [child['row_num'] for child in parent['children']]
        if 62 in row_nums and 63 in row_nums:
            print("  ✅ 子元素包含行62和行63")
        else:
            print("  ❌ 子元素不包含行62和行63")
        break
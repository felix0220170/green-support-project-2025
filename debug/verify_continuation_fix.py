import json

# 读取修改后的两层结构数据
file_path = '../src/output/modified_two_level_structure.json'
with open(file_path, 'r', encoding='utf-8') as f:
    modified_data = json.load(f)

print("验证续行修复效果：")
print("\n1. 查找B='3515'的子元素：")

# 查找B=3515的子元素
for parent in modified_data:
    for child in parent['children']:
        if child['B'] == '3515':
            print(f"   找到子元素：")
            print(f"   B: {child['B']}")
            print(f"   C: {child['C']}")
            print(f"   D列开头: {child['D'][:100]}...")
            print(f"   D列结尾: ...{child['D'][-200:]:.200}")
            print(f"   D列长度: {len(child['D'])} 字符")
            
            # 检查D列是否包含完整内容
            if '利用可燃固体废物部分或全部替代煤炭等燃料' in child['D']:
                print("   ✅ D列包含完整内容")
            else:
                print("   ❌ D列不包含完整内容")
            
            print()

# 2. 检查是否存在B='0000'且C为None的子元素
print("\n2. 检查是否存在B='0000'且C为None的子元素：")
b_zero_found = False
for parent in modified_data:
    for child in parent['children']:
        if child['B'] == '0000' and child['C'] is None:
            print(f"   ❌ 发现B='0000'且C为None的子元素：")
            print(f"   父元素: {parent['category_name']}")
            print(f"   B: {child['B']}")
            print(f"   C: {child['C']}")
            print(f"   D列开头: {child['D'][:100]}...")
            print()
            b_zero_found = True
            break
    if b_zero_found:
        break

if not b_zero_found:
    print("   ✅ 未发现B='0000'且C为None的子元素")

# 3. 检查原始行39和40是否已经合并
print("\n3. 检查原始行39和40是否已经合并：")
parsed_file_path = '../src/output/parsed_excel_rows.json'
with open(parsed_file_path, 'r', encoding='utf-8') as f:
    parsed_data = json.load(f)

row_39_found = False
row_40_found = False
for row in parsed_data:
    if row['row_num'] == 39:
        row_39_found = True
        print(f"   row_num=39: 存在")
    elif row['row_num'] == 40:
        row_40_found = True
        print(f"   row_num=40: 存在")

if row_39_found and not row_40_found:
    print("   ✅ row_num=40已被合并到row_num=39")
else:
    print("   ❌ 合并可能未成功")

import json

# 读取清理后的两层结构数据
cleaned_file_path = '../src/output/cleaned_two_level_structure.json'
with open(cleaned_file_path, 'r', encoding='utf-8') as f:
    cleaned_data = json.load(f)

print("验证清理后的数据：")

# 1. 检查是否存在B='0000'且C为None的子元素
print("\n1. 检查是否存在B='0000'且C为None的子元素：")
b_zero_found = False
for parent in cleaned_data:
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

# 2. 检查原始问题（B='3515'的子元素）是否仍然正确
print("\n2. 检查B='3515'的子元素：")
for parent in cleaned_data:
    for child in parent['children']:
        if child['B'] == '3515':
            print(f"   ✅ 找到B='3515'的子元素：")
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

# 3. 检查原始的行62和行63是否仍然存在
print("\n3. 检查原始的行62和行63是否仍然存在：")
# 首先需要在原始解析数据中找到这些行对应的B值
parsed_file_path = '../src/output/parsed_excel_rows.json'
with open(parsed_file_path, 'r', encoding='utf-8') as f:
    parsed_data = json.load(f)

# 查找行62和行63对应的B值
row_62_b = None
row_63_b = None
for row in parsed_data:
    if row['row_num'] == 62:
        row_62_b = row['B']
    elif row['row_num'] == 63:
        row_63_b = row['B']

if row_62_b and row_63_b:
    # 转换为4位字符串格式
    row_62_b_str = f"{row_62_b:04d}"
    row_63_b_str = f"{row_63_b:04d}"
    
    print(f"   行62的B值: {row_62_b_str}")
    print(f"   行63的B值: {row_63_b_str}")
    
    # 在清理后的数据中查找这些B值
    row_62_found = False
    row_63_found = False
    for parent in cleaned_data:
        for child in parent['children']:
            if child['B'] == row_62_b_str:
                row_62_found = True
            elif child['B'] == row_63_b_str:
                row_63_found = True
    
    if row_62_found and row_63_found:
        print("   ✅ 行62和行63对应的子元素仍然存在")
    else:
        print(f"   ❌ 行62: {'存在' if row_62_found else '不存在'}")
        print(f"   ❌ 行63: {'存在' if row_63_found else '不存在'}")

# 4. 检查数据统计
print("\n4. 数据统计：")
print(f"   父元素数量: {len(cleaned_data)}")
print(f"   子元素总数量: {sum(len(parent['children']) for parent in cleaned_data)}")

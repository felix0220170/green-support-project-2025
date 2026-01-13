import json

# 读取最终的两层结构数据
final_file_path = '../src/output/final_two_level_structure.json'
with open(final_file_path, 'r', encoding='utf-8') as f:
    final_data = json.load(f)

print("验证最终结构数据：")

# 1. 检查是否还有父元素的category_name包含category_id
print("\n1. 检查父元素的category_name是否已去掉category_id：")
contains_id_found = False
for parent in final_data:
    category_id = parent['category_id']
    category_name = parent['category_name']
    
    if category_id in category_name:
        print(f"   ❌ 发现category_name仍然包含category_id：")
        print(f"      category_id: {category_id}")
        print(f"      category_name: {category_name}")
        contains_id_found = True
        break

if not contains_id_found:
    print("   ✅ 所有父元素的category_name都已去掉category_id部分")

# 2. 检查修改后的category_name格式
print("\n2. 检查修改后的category_name格式：")
for i, parent in enumerate(final_data[:10]):
    print(f"   {i+1}. category_id: {parent['category_id']}")
    print(f"      category_name: {parent['category_name']}")

# 3. 检查之前的问题元素是否仍然正确
print("\n3. 检查之前的问题元素：")

# 检查B='3515'的子元素
print("   a. 检查B='3515'的子元素：")
for parent in final_data:
    for child in parent['children']:
        if child['B'] == '3515':
            print(f"      ✅ 找到B='3515'的子元素：")
            print(f"         父元素: {parent['category_name']}")
            print(f"         B: {child['B']}")
            print(f"         C: {child['C']}")
            break
    else:
        continue
    break

# 检查1.1.17父元素
print("\n   b. 检查1.1.17父元素：")
for parent in final_data:
    if parent['category_id'] == '1.1.17':
        print(f"      ✅ 找到1.1.17父元素：")
        print(f"         category_id: {parent['category_id']}")
        print(f"         category_name: {parent['category_name']}")
        print(f"         子元素数量: {len(parent['children'])}")
        break

# 4. 数据统计
print("\n4. 数据统计：")
print(f"   父元素数量: {len(final_data)}")
print(f"   子元素总数量: {sum(len(parent['children']) for parent in final_data)}")

import json

# 读取修改后的两层结构数据
file_path = '../src/output/modified_two_level_structure.json'
with open(file_path, 'r', encoding='utf-8') as f:
    modified_data = json.load(f)

# 读取原始数据作为对比
original_file_path = '../src/output/two_level_structure.json'
with open(original_file_path, 'r', encoding='utf-8') as f:
    original_data = json.load(f)

print("验证修改结果：")

# 1. 检查是否去掉了row_num属性
print("\n1. 检查是否去掉了row_num属性：")
row_num_found = False
for parent in modified_data:
    for child in parent['children']:
        if 'row_num' in child:
            print(f"  ❌ 发现row_num属性：{child['row_num']}")
            row_num_found = True
            break
    if row_num_found:
        break
if not row_num_found:
    print("  ✅ 所有元素的row_num属性已去掉")

# 2. 检查F列值是否转换正确
print("\n2. 检查F列值是否转换正确：")
f_conversion_ok = True
for orig_parent, mod_parent in zip(original_data, modified_data):
    for orig_child, mod_child in zip(orig_parent['children'], mod_parent['children']):
        orig_f = orig_child.get('F', '')
        mod_f = mod_child.get('F', 0)
        
        expected = 0
        if orig_f == '√':
            expected = 1
        elif orig_f == '√√':
            expected = 2
        
        if mod_f != expected:
            print(f"  ❌ F列转换错误：原始值='{orig_f}', 修改后={mod_f}, 期望值={expected}")
            f_conversion_ok = False
            break
    if not f_conversion_ok:
        break
if f_conversion_ok:
    print("  ✅ F列值转换正确")

# 3. 检查B列值是否转换为4位字符串并保留前导零
print("\n3. 检查B列值是否转换为4位字符串并保留前导零：")
b_conversion_ok = True
for orig_parent, mod_parent in zip(original_data, modified_data):
    for orig_child, mod_child in zip(orig_parent['children'], mod_parent['children']):
        orig_b = orig_child.get('B', '')
        mod_b = mod_child.get('B', '')
        
        if not isinstance(mod_b, str) or len(mod_b) != 4:
            print(f"  ❌ B列格式错误：原始值={orig_b}, 修改后={mod_b} (类型={type(mod_b).__name__})")
            b_conversion_ok = False
            break
            
        # 检查是否可以转换为数字，并且是否保留了前导零
        try:
            int_value = int(mod_b)
            if len(str(int_value)) < 4 and not mod_b.startswith('0'):
                print(f"  ❌ B列前导零丢失：原始值={orig_b}, 修改后={mod_b}")
                b_conversion_ok = False
                break
        except ValueError:
            print(f"  ❌ B列不是数字字符串：原始值={orig_b}, 修改后={mod_b}")
            b_conversion_ok = False
            break
    if not b_conversion_ok:
        break
if b_conversion_ok:
    print("  ✅ B列值已转换为4位字符串并保留前导零")

# 4. 检查1.1.1父元素的子元素（包含B=3411的子元素）
print("\n4. 检查1.1.1父元素的子元素：")
for parent in modified_data:
    if parent['category_id'] == '1.1.1':
        print(f"  父元素: {parent['category_name']}")
        print(f"  子元素数量: {len(parent['children'])}")
        
        for i, child in enumerate(parent['children']):
            print(f"    子元素 {i+1}:")
            print(f"      B: {child['B']} (类型: {type(child['B']).__name__})")
            print(f"      F: {child['F']} (类型: {type(child['F']).__name__})")
            print(f"      是否包含row_num: {'是' if 'row_num' in child else '否'}")
        break

# 5. 检查是否有F列值为2的情况（√√）
print("\n5. 检查F列值为2的情况：")
f_two_found = False
for parent in modified_data:
    for child in parent['children']:
        if child.get('F') == 2:
            print(f"  ✅ 找到F列值为2的子元素：")
            print(f"    父元素: {parent['category_name']}")
            print(f"    B: {child['B']}")
            print(f"    F: {child['F']}")
            f_two_found = True
            break
    if f_two_found:
        break
if not f_two_found:
    print("  ⚠️  未找到F列值为2的子元素")

# 6. 检查B列值小于1000的情况，确保前导零保留
print("\n6. 检查B列值小于1000的情况：")
leading_zero_found = False
for parent in modified_data:
    for child in parent['children']:
        b_value = child.get('B', '')
        if isinstance(b_value, str) and len(b_value) == 4 and b_value.startswith('0'):
            print(f"  ✅ 找到保留前导零的B列值：{b_value}")
            leading_zero_found = True
            break
    if leading_zero_found:
        break
if not leading_zero_found:
    print("  ⚠️  未找到保留前导零的B列值")

print("\n验证完成！")

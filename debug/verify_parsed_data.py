import json

# 读取解析后的数据
file_path = '../src/output/parsed_excel_rows.json'
with open(file_path, 'r', encoding='utf-8') as f:
    parsed_rows = json.load(f)

print(f"共解析了 {len(parsed_rows)} 行数据")

# 1. 检查standard字段是否都不为空
print("\n1. 检查standard字段是否都不为空：")
empty_standard_count = 0
for row in parsed_rows:
    if row['D'] is None:
        empty_standard_count += 1
        print(f"   行 {row['row_num']} 的standard字段为空")

if empty_standard_count == 0:
    print("   ✅ 所有行的standard字段都不为空")
else:
    print(f"   ❌ 发现 {empty_standard_count} 行的standard字段为空")

# 2. 检查remark字段的情况
print("\n2. 检查remark字段的情况：")
empty_remark_count = 0
for row in parsed_rows:
    if row['E'] is None:
        empty_remark_count += 1

print(f"   共有 {empty_remark_count} 行的remark字段为空，{len(parsed_rows) - empty_remark_count} 行的remark字段不为空")

# 3. 查看前20行数据
print("\n3. 前20行数据预览：")
for i, row in enumerate(parsed_rows[:20]):
    print(f"   行 {row['row_num']}：")
    print(f"     A: {row['A']}")
    print(f"     B: {row['B']}")
    print(f"     C: {row['C']}")
    print(f"     D: {row['D'][:50]}..." if row['D'] and isinstance(row['D'], str) and len(row['D']) > 50 else f"     D: {row['D']}")
    print(f"     E: {row['E'][:50]}..." if row['E'] and isinstance(row['E'], str) and len(row['E']) > 50 else f"     E: {row['E']}")
    print(f"     F: {row['F']}")
    print()

# 4. 检查特定行（用户之前提到的2.2.7行）
print("\n4. 检查特定行（2.2.7相关行）：")
for row in parsed_rows:
    if row['A'] and isinstance(row['A'], str) and '2.2.7' in row['A']:
        print(f"   找到2.2.7行：行 {row['row_num']}")
        print(f"     A: {row['A']}")
        print(f"     B: {row['B']}")
        print(f"     C: {row['C']}")
        print(f"     D: {row['D']}")
        print(f"     E: {row['E']}")
        print(f"     F: {row['F']}")
        print()

# 5. 检查断句拼接是否正确（寻找包含特定文本的行）
print("\n5. 检查断句拼接是否正确：")
for i, row in enumerate(parsed_rows):
    if i > 0 and row['D'] and isinstance(row['D'], str):
        # 检查是否有拼接的痕迹
        if len(row['D']) > 100:
            print(f"   行 {row['row_num']} 的D字段长度为 {len(row['D'])} 字符")
            print(f"     内容：{row['D'][:100]}...")
            print()
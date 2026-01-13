import json

# 读取原始解析数据
parsed_file_path = '../src/output/parsed_excel_rows.json'
with open(parsed_file_path, 'r', encoding='utf-8') as f:
    parsed_data = json.load(f)

# 查找包含特定D列内容的行
print("查找包含特定D列内容的行：")
print("1. 查找包含'利用可燃固体废物'的行：")
for row in parsed_data:
    if row['D'] and isinstance(row['D'], str) and '利用可燃固体废物' in row['D']:
        print(f"   row_num: {row['row_num']}")
        print(f"   A: {row['A']}")
        print(f"   B: {row['B']}")
        print(f"   C: {row['C']}")
        print(f"   D: {row['D'][:200]}...")
        print(f"   E: {row['E'][:100]}..." if row['E'] and isinstance(row['E'], str) else f"   E: {row['E']}")
        print(f"   F: {row['F']}")
        print()

print("2. 查找包含'采用替代燃料技术'的行：")
for row in parsed_data:
    if row['D'] and isinstance(row['D'], str) and '采用替代燃料技术' in row['D']:
        print(f"   row_num: {row['row_num']}")
        print(f"   A: {row['A']}")
        print(f"   B: {row['B']}")
        print(f"   C: {row['C']}")
        print(f"   D: {row['D'][:200]}...")
        print(f"   E: {row['E'][:100]}..." if row['E'] and isinstance(row['E'], str) else f"   E: {row['E']}")
        print(f"   F: {row['F']}")
        print()

# 查看row_num=40的行
print("3. 查看row_num=40的行：")
for row in parsed_data:
    if row['row_num'] == 40:
        print(f"   row_num: {row['row_num']}")
        print(f"   A: {row['A']}")
        print(f"   B: {row['B']}")
        print(f"   C: {row['C']}")
        print(f"   D: {row['D'][:200]}..." if row['D'] and isinstance(row['D'], str) else f"   D: {row['D']}")
        print(f"   E: {row['E'][:100]}..." if row['E'] and isinstance(row['E'], str) else f"   E: {row['E']}")
        print(f"   F: {row['F']}")
        print()
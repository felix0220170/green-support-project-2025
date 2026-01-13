import json

# 读取原始解析数据
parsed_file_path = '../src/output/parsed_excel_rows.json'
with open(parsed_file_path, 'r', encoding='utf-8') as f:
    parsed_data = json.load(f)

# 查找包含特定D列内容的行
print("查找包含'消耗臭氧潜能值'的行：")
for row in parsed_data:
    if row['D'] and isinstance(row['D'], str) and '消耗臭氧潜能值' in row['D']:
        print(f"   row_num: {row['row_num']}")
        print(f"   A: {row['A']}")
        print(f"   B: {row['B']}")
        print(f"   C: {row['C']}")
        print(f"   D: {row['D'][:200]}...")
        print(f"   E: {row['E'][:100]}..." if row['E'] and isinstance(row['E'], str) else f"   E: {row['E']}")
        print(f"   F: {row['F']}")
        print()

# 查找行号在新发现的B='0000'子元素附近的行
print("查找行号在40-50之间的行：")
for row in parsed_data:
    if 40 <= row['row_num'] <= 50:
        print(f"   row_num: {row['row_num']}")
        print(f"   A: {row['A'][:50]}..." if row['A'] and isinstance(row['A'], str) else f"   A: {row['A']}")
        print(f"   B: {row['B']}")
        print(f"   C: {row['C']}")
        print(f"   D: {row['D'][:50]}..." if row['D'] and isinstance(row['D'], str) else f"   D: {row['D']}")
        print(f"   E: {row['E']}")
        print(f"   F: {row['F']}")
        print()
import json

# 读取修复后的解析数据
file_path = '../src/output/parsed_excel_rows.json'
with open(file_path, 'r', encoding='utf-8') as f:
    parsed_data = json.load(f)

# 查找row_num为2的数据
print("查找row_num为2的数据：")
for row in parsed_data:
    if row['row_num'] == 2:
        print(json.dumps(row, ensure_ascii=False, indent=2))
        break

# 查找row_num为5之前的几行数据
print("\n查找row_num <= 5的数据：")
for row in parsed_data:
    if row['row_num'] <= 5:
        print(f"\nrow_num: {row['row_num']}")
        print(f"A: {row['A']}")
        print(f"D: {row['D'][:50]}..." if row['D'] and isinstance(row['D'], str) else f"D: {row['D']}")
        print(f"类型: {'父元素' if row['A'] and isinstance(row['A'], str) and '1.1.1' in row['A'] else '普通行'}")
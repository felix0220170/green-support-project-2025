import json

# 读取修复后的解析数据
file_path = '../src/output/parsed_excel_rows.json'
with open(file_path, 'r', encoding='utf-8') as f:
    parsed_data = json.load(f)

# 查找row_num为5的数据
print("查找row_num为5的数据：")
for row in parsed_data:
    if row['row_num'] == 5:
        print(json.dumps(row, ensure_ascii=False, indent=2))
        break

# 检查B=3411的数据
print("\n查找B=3411的数据：")
for row in parsed_data:
    if row['B'] == 3411:
        print(json.dumps(row, ensure_ascii=False, indent=2))
        break
import json

# 读取原始解析数据
file_path = '../src/output/parsed_excel_rows.json'
with open(file_path, 'r', encoding='utf-8') as f:
    parsed_data = json.load(f)

# 查找第4行的数据
print("查找第4行的数据：")
for row in parsed_data:
    if row['row_num'] == 4:
        print(json.dumps(row, ensure_ascii=False, indent=2))
        break

# 查找第3行的数据，作为参考
print("\n查找第3行的数据：")
for row in parsed_data:
    if row['row_num'] == 3:
        print(json.dumps(row, ensure_ascii=False, indent=2))
        break
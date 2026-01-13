import pandas as pd
import re
import json

# 直接读取Excel文件并处理索引为220的行
df = pd.read_excel('green_finance_2025.xlsx', sheet_name=0, header=None)

# 直接获取索引为220的行
target_row = df.iloc[220]

print(f"=== 直接测试索引为220的行 ===")
print(f"A列内容: {repr(target_row.iloc[0])}")
print(f"类型: {type(target_row.iloc[0])}")

# 模拟convert.py中的处理逻辑
print(f"\n=== 模拟convert.py中的处理逻辑 ===")

# 清洗当前行数据
category_text = str(target_row.iloc[0]) if not pd.isna(target_row.iloc[0]) else ""
industry_name = str(target_row.iloc[2]).strip() if not pd.isna(target_row.iloc[2]) else ""
standard = str(target_row.iloc[3]) if not pd.isna(target_row.iloc[3]) else ""
remark = str(target_row.iloc[4]) if not pd.isna(target_row.iloc[4]) else ""
original_industry_codes = target_row.iloc[1]
original_remark = target_row.iloc[4]

print(f"清洗后的数据:")
print(f"   category_text: {repr(category_text)}")
print(f"   industry_name: {repr(industry_name)}")
print(f"   standard: {repr(standard[:50])}...")
print(f"   remark: {repr(remark[:50])}...")

# 检查是否是新的三级ID大分类
print(f"\n检查是否是新的三级ID大分类:")

# 先清理干扰字符和多余空格
cleaned_text = re.sub(r'[^\d\.\s\u4e00-\u9fa5]', '', category_text)
print(f"   cleaned_text: {repr(cleaned_text)}")

# 压缩连续空格
cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
print(f"   cleaned_text（压缩空格）: {repr(cleaned_text)}")

# 使用match从开头匹配
match = re.match(r'([\d\.]+)\s+(.*)', cleaned_text)
print(f"   match对象: {match}")

if match:
    category_id = match.group(1)
    category_name = match.group(2)
    print(f"   category_id: {repr(category_id)}")
    print(f"   category_name: {repr(category_name)}")

# 检查是否是三级ID
print(f"\n检查是否是三级ID:")
print(f"   re.search(r'\d+\.\d+\.\d+', category_id): {re.search(r'\d+\.\d+\.\d+', category_id)}")

# 从E列提取代码
print(f"\n从E列提取代码:")

all_remarks = str(original_remark) if not pd.isna(original_remark) else ""
print(f"   all_remarks: {repr(all_remarks[:100])}...")

if all_remarks:
    # 使用相同的正则表达式
    codes_from_e = re.findall(r'\b\d{3,4}\b', all_remarks)
    codes_from_e = [code.zfill(4) for code in codes_from_e]
    print(f"   提取的代码: {codes_from_e}")
    print(f"   包含0311: {'0311' in codes_from_e}")

# 现在让我们检查convert.py的result中是否应该包含这个条目
print(f"\n=== 检查最终结果 ===")

# 读取生成的JSON文件
with open('green_finance_2025.json', 'r', encoding='utf-8') as f:
    result = json.load(f)

# 检查0311中是否有2.2.7
print(f"检查0311中是否有2.2.7:")
if '0311' in result:
    found = False
    for item in result['0311']:
        if item['categoryId'] == '2.2.7':
            print(f"✅ 找到2.2.7在0311中")
            found = True
            break
    if not found:
        print(f"❌ 0311中没有2.2.7")
        print(f"0311中的所有categoryId:")
        for item in result['0311']:
            print(f"   - {item['categoryId']} ({item['categoryName']})")

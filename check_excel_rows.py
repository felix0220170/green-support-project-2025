import pandas as pd

# 直接读取Excel文件
df = pd.read_excel('green_finance_2025.xlsx', sheet_name=0, header=None)

print(f"Excel文件总行数: {len(df)}")
print(f"\n=== 检查行索引和A列内容 ===")

# 检查索引为215到225之间的行
for idx in range(215, 226):
    if idx < len(df):
        row = df.iloc[idx]
        a_col = row.iloc[0]
        print(f"索引 {idx}（行号 {idx+1}）: {repr(a_col)}")
        print(f"   类型: {type(a_col)}")
        print(f"   包含'2.2.7': {'2.2.7' in str(a_col)}")

# 特别检查索引为220的行
print(f"\n=== 特别检查索引为220的行 ===")
if 220 < len(df):
    row = df.iloc[220]
    print(f"索引 220（行号 221）:")
    print(f"   A列: {repr(row.iloc[0])}")
    print(f"   B列: {repr(row.iloc[1])}")
    print(f"   C列: {repr(row.iloc[2])}")
    print(f"   D列: {repr(row.iloc[3][:50] if not pd.isna(row.iloc[3]) else '')}...")
    print(f"   E列: {repr(row.iloc[4][:50] if not pd.isna(row.iloc[4]) else '')}...")

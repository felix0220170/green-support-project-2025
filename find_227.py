import pandas as pd

# 读取Excel文件
df = pd.read_excel('green_finance_2025.xlsx', sheet_name=0, header=None)

print(f"Excel文件总行数: {len(df)}")
print(f"\n=== 查找2.2.7行 ===")

# 遍历所有行，查找2.2.7
found = False
for idx, row in df.iterrows():
    # 只打印匹配行，避免输出过多
    if idx % 100 == 0:
        print(f"   已检查 {idx} 行...")
    
    a_col = row.iloc[0]
    str_a_col = str(a_col)
    
    # 直接检查是否包含2.2.7
    if '2.2.7' in str_a_col:
        print(f"\n找到2.2.7行:")
        print(f"   索引: {idx}（行号: {idx+1}）")
        print(f"   A列内容: {repr(a_col)}")
        print(f"   类型: {type(a_col)}")
        print(f"   转换为字符串: {repr(str_a_col)}")
        
        # 打印完整的行信息
        print(f"\n   完整行信息:")
        print(f"      A列: {repr(a_col)}")
        print(f"      B列: {repr(row.iloc[1])}")
        print(f"      C列: {repr(row.iloc[2])}")
        print(f"      D列: {repr(row.iloc[3][:100] if not pd.isna(row.iloc[3]) else '')}...")
        print(f"      E列: {repr(row.iloc[4][:100] if not pd.isna(row.iloc[4]) else '')}...")
        
        found = True
        break
    
    # 同时检查是否包含2.2，用于调试
    elif '2.2' in str_a_col:
        print(f"\n找到包含2.2的行:")
        print(f"   索引: {idx}（行号: {idx+1}）")
        print(f"   A列内容: {repr(a_col)}")

if not found:
    print("\n未找到2.2.7行。让我打印前50行的A列内容:")
    for idx, row in df.iterrows():
        if idx >= 50:
            break
        a_col = row.iloc[0]
        print(f"   行 {idx+1}: {repr(a_col)}")

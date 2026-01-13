import pandas as pd
import re

def check_227_row():
    # 读取Excel文件
    df = pd.read_excel('green_finance_2025.xlsx', sheet_name=0, header=None)
    
    print("查找2.2.7相关行：")
    for idx, row in df.iterrows():
        category = str(row.iloc[0]).strip() if not pd.isna(row.iloc[0]) else ''
        if re.match(r'^2\.2\.7', category):
            print(f"行 {idx+1}: A列={category}")
            # 打印该行的详细内容
            a_col = str(row.iloc[0]).strip() if not pd.isna(row.iloc[0]) else ''
            b_col = str(row.iloc[1]).strip() if not pd.isna(row.iloc[1]) else ''
            c_col = str(row.iloc[2]).strip() if not pd.isna(row.iloc[2]) else ''
            d_col = str(row.iloc[3]).strip() if not pd.isna(row.iloc[3]) else ''
            e_col = str(row.iloc[4]).strip() if not pd.isna(row.iloc[4]) else ''
            print(f"  行 {idx+1}详细内容:")
            print(f"    A列: {a_col}")
            print(f"    B列: {b_col}")
            print(f"    C列: {c_col}")
            print(f"    D列: {d_col[:100]}...")
            print(f"    E列: {e_col[:100]}...")
            print(f"    E列包含0311: {'0311' in e_col}")
            # 打印E列中0311前后的字符，检查单词边界
            if '0311' in e_col:
                index = e_col.index('0311')
                # 打印0311前后的5个字符
                start = max(0, index-5)
                end = min(len(e_col), index+7)
                print(f"    0311前后字符: '{e_col[start:end]}'")
                print(f"    0311前面的字符: '{e_col[start:index]}' (类型: {repr(e_col[start:index])})")
                print(f"    0311后面的字符: '{e_col[index+4:end]}' (类型: {repr(e_col[index+4:end])})")
            
            # 测试正则表达式匹配
            test_matches = re.findall(r'\b\d{3,4}\b', e_col)
            print(f"    正则匹配结果: {test_matches}")
            
            # 打印前5行和后5行，查看上下文
            print(f"\n  上下文行（前5行到后5行）：")
            for i in range(max(0, idx-5), min(idx+6, len(df))):
                r = df.iloc[i]
                a = str(r.iloc[0]).strip() if not pd.isna(r.iloc[0]) else ''
                b = str(r.iloc[1]).strip() if not pd.isna(r.iloc[1]) else ''
                c = str(r.iloc[2]).strip() if not pd.isna(r.iloc[2]) else ''
                d = str(r.iloc[3]).strip() if not pd.isna(r.iloc[3]) else ''
                e = str(r.iloc[4]).strip() if not pd.isna(r.iloc[4]) else ''
                
                # 标记当前行
                marker = "-> " if i == idx else "   "
                
                # 格式化输出
                print(f"    {marker}行 {i+1}: A={a}, B={b}, C={c}, E包含0311: {'0311' in e}")
            
            break

def check_227_in_json():
    import json
    with open('green_finance_2025.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("\n=== 检查2.2.7在JSON中的出现情况 ===")
    
    # 检查0311中是否有2.2.7
    print("\n1. 检查0311中是否有2.2.7:")
    if '0311' in data:
        found = False
        for i, item in enumerate(data['0311']):
            if item['categoryId'] == '2.2.7':
                print(f"   ✅ 找到2.2.7在0311的第{i+1}项")
                print(f"      完整项: {json.dumps(item, ensure_ascii=False, indent=2)}")
                found = True
                break
        if not found:
            print("   ❌ 0311中没有2.2.7")
            print("   0311中的所有categoryId:")
            for item in data['0311']:
                print(f"      - {item['categoryId']} ({item['categoryName']})")
    else:
        print("   ❌ 0311不存在")
    
    # 检查是否有其他代码关联到2.2.7
    print("\n2. 检查所有关联到2.2.7的代码:")
    found = False
    for code, items in data.items():
        for item in items:
            if item['categoryId'] == '2.2.7':
                print(f"   - 代码 {code} 关联到2.2.7")
                found = True
    if not found:
        print("   ❌ 没有代码关联到2.2.7")

def check_227_position_in_excel():
    import pandas as pd
    
    print("\n=== 检查2.2.7在Excel中的位置 ===")
    
    # 读取Excel文件
    df = pd.read_excel('green_finance_2025.xlsx', sheet_name=0, header=None)
    
    # 查找2.2.7行
    target_idx = None
    for idx, row in df.iterrows():
        category = str(row.iloc[0]).strip() if not pd.isna(row.iloc[0]) else ''
        if '2.2.7' in category:
            target_idx = idx
            break
    
    if target_idx is None:
        print("❌ 未找到2.2.7行")
        return
    
    print(f"2.2.7行索引: {target_idx} (行号: {target_idx+1})")
    print(f"Excel文件总行数: {len(df)}")
    
    # 检查是否是最后几行
    if target_idx >= len(df) - 10:
        print(f"2.2.7行位于Excel文件的最后10行内")
        
        # 显示最后10行的A列内容
        print("\n最后10行的A列内容:")
        for idx in range(max(0, len(df)-10), len(df)):
            row = df.iloc[idx]
            category = str(row.iloc[0]).strip() if not pd.isna(row.iloc[0]) else ''
            marker = "->" if idx == target_idx else "  "
            print(f"   {marker}行 {idx+1}: A列 = '{category}'")

if __name__ == "__main__":
    check_227_row()
    check_227_in_json()
    check_227_position_in_excel()

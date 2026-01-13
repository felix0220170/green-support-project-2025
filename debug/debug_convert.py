import pandas as pd
import re
import json

def clean_text(text, remove_hanzi_spaces=False):
    if pd.isna(text):
        return ""
    text = str(text)
    # 移除首尾空格
    text = text.strip()
    # 移除制表符
    text = text.replace("\t", " ")
    # 移除换行符
    text = text.replace("\n", " ")
    # 移除多余空格
    text = re.sub(r"\s+", " ", text)
    # 如果需要，移除汉字间的空格
    if remove_hanzi_spaces:
        text = re.sub(r"([\u4e00-\u9fa5])\s+([\u4e00-\u9fa5])", r"\1\2", text)
    return text

def process_current_entry(entry, result):
    """处理当前子项，提取行业代码并生成JSON"""
    # 提取行业代码
    industry_codes = []
    
    # 从B列提取原始行业代码
    if not pd.isna(entry['original_industry_codes']):
        original_code_str = str(entry['original_industry_codes'])
        # 匹配数字代码，如111, 112, 0111, 0112
        codes = re.findall(r'\b\d{3,4}\b', original_code_str)
        industry_codes.extend(codes)
    
    # 从E列提取行业代码
    codes_from_e = []
    if entry['original_remark_parts']:
        all_remarks = ""
        for original_remark in entry['original_remark_parts']:
            if not pd.isna(original_remark):
                all_remarks += str(original_remark) + ' '
        # 匹配数字代码，如111, 112, 0111, 0112
        codes_from_e = re.findall(r'\b\d{3,4}\b', all_remarks)
        industry_codes.extend(codes_from_e)
    
    # 特别处理2.2.7行
    if entry['category_id'] == '2.2.7':
        print(f"\n=== 调试2.2.7行的process_current_entry函数 ===")
        print(f"   category_id: {entry['category_id']}")
        print(f"   从B列提取的代码: {industry_codes}")
        print(f"   从E列提取的代码: {codes_from_e}")
        print(f"   包含0311: {'0311' in codes_from_e}")
    
    # 去重并补零到4位
    industry_codes = list(set(industry_codes))
    industry_codes = [code.zfill(4) for code in industry_codes]
    
    # 如果没有行业代码，跳过
    if not industry_codes:
        return
    
    # 提取温室气体减排贡献等级
    contribution_level = 0
    if not pd.isna(entry['original_contribution']):
        contribution_text = str(entry['original_contribution']).strip()
        if contribution_text == "低碳赋能":
            contribution_level = 1
        elif contribution_text == "直接减排":
            contribution_level = 2
    
    # 生成JSON结构
    for code in industry_codes:
        if code not in result:
            result[code] = []
        
        # 构建当前项
        current_item = {
            "categoryId": entry['category_id'],
            "categoryName": entry['category_name'],
            "industryName": entry['industry_name'],
            "standard": entry['standard'],
            "remark": entry['remark'],
            "contributionLevel": contribution_level
        }
        
        # 特别处理2.2.7行
        if entry['category_id'] == '2.2.7' and code == '0311':
            print(f"\n=== 向JSON中添加2.2.7和0311的关联 ===")
            print(f"   当前项: {current_item}")
        
        result[code].append(current_item)

# 主函数
def main():
    # 读取Excel文件
    df = pd.read_excel('../src/green_finance_2025.xlsx', sheet_name=0, header=None)
    
    result = {}
    current_category = None  # 当前大分类
    current_entry = None     # 当前处理的子项
    
    print("正在执行智能子项识别处理...")
    
    # 遍历所有行
    print(f"\n=== 开始遍历Excel行 ===")
    print(f"Excel文件总行数: {len(df)}")
    row_count = 0
    
    # 只处理索引215到225之间的行
    for idx, row in df.iterrows():
        if idx < 215 or idx > 225:
            continue
            
        row_count += 1
        
        print(f"\n=== 处理行（索引{idx}，行号{row_count}） ===")
        print(f"   A列内容: {repr(row.iloc[0])}")
        
        # 特别处理2.2.7行（索引220）
        is_target_row = idx == 220
        if is_target_row:
            print(f"   ===>>> 目标行2.2.7 <<<===")
        
        # 获取原始行数据
        original_category = row.iloc[0]  # A列：领域
        original_industry_codes = row.iloc[1]  # B列：行业代码
        original_industry_name = row.iloc[2]  # C列：行业名称
        original_standard = row.iloc[3]  # D列：条件/标准
        original_remark = row.iloc[4]  # E列：备注
        original_contribution = row.iloc[5]  # F列：温室气体减排标识
        
        if is_target_row:
            print(f"   原始行数据:")
            print(f"      A列: {repr(original_category)}")
            print(f"      B列: {repr(original_industry_codes)}")
            print(f"      C列: {repr(original_industry_name)}")
            print(f"      D列: {repr(original_standard[:50] if not pd.isna(original_standard) else '')}...")
            print(f"      E列: {repr(original_remark[:50] if not pd.isna(original_remark) else '')}...")
        
        # 清洗当前行数据
        category_text = str(original_category) if not pd.isna(original_category) else ""
        industry_name = clean_text(original_industry_name, remove_hanzi_spaces=True)
        standard = clean_text(original_standard)
        remark = clean_text(original_remark)
        
        # 跳过表头行
        if category_text == "领域" and industry_name == "国民经济行业类别名称":
            continue
        
        # 检查是否是新的三级ID大分类（x.y.z格式）
        is_new_category = False
        new_category = None
        
        if category_text.strip():
            # 先清理干扰字符和多余空格，强化ID捕获
            # 移除所有非数字、非点号、非空格和非中文字符
            cleaned_text = re.sub(r'[^\d\.\s\u4e00-\u9fa5]', '', category_text)
            # 压缩连续空格
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
            
            # 使用match从开头匹配，确保正确提取ID和名称
            match = re.match(r'([\d\.]+)\s+(.*)', cleaned_text)
            if match:
                category_id = match.group(1)
                category_name = match.group(2)
            else:
                # 尝试手动分割
                space_pos = cleaned_text.find(' ')
                if space_pos != -1:
                    category_id = cleaned_text[:space_pos]
                    category_name = cleaned_text[space_pos+1:]
                else:
                    category_id = cleaned_text
                    category_name = ""
            
            # 清洗结果
            category_id = clean_text(category_id).replace(' ', '')
            category_name = clean_text(category_name, remove_hanzi_spaces=True)
            
            # 检查是否是三级ID
            # 使用search代替match，在整个字符串中搜索匹配的模式
            if re.search(r'\d+\.\d+\.\d+', category_id):
                new_category = {
                    'category_id': category_id,
                    'category_name': category_name
                }
                is_new_category = True
        
        # 处理新的大分类
        if is_new_category:
            # 更新当前分类
            current_category = new_category
            print(f"\n调试：发现新的大分类")
            print(f"   category_id: {current_category['category_id']}")
            print(f"   category_name: {current_category['category_name']}")
            # 重置当前子项
            current_entry = None
            # 新分类开启时，强制创建一个新子项来捕获首行内容
            force_new_entry = True
        else:
            force_new_entry = False
        
        # 检查是否是新子项（B列或C列不为空）
        has_industry_code = not pd.isna(original_industry_codes) and str(original_industry_codes).strip() not in ['', '-']
        has_industry_name = industry_name.strip() != ''
        is_new_entry = has_industry_code or has_industry_name or force_new_entry
    
        print(f"   检查是否是新子项:")
        print(f"      has_industry_code: {has_industry_code}")
        print(f"      has_industry_name: {has_industry_name}")
        print(f"      force_new_entry: {force_new_entry}")
        print(f"      is_new_entry: {is_new_entry}")
        print(f"      current_entry存在: {current_entry is not None}")
        
        # 处理A、B、C同时为空的情况 - 追加到上一个子项
        a_b_c_empty = not category_text.strip() and not has_industry_code and not has_industry_name
        if a_b_c_empty and current_entry:
            print(f"   A、B、C同时为空，追加到上一个子项")
            # 追加标准文本
            if standard:
                current_entry['standard'] += standard
            # 追加备注文本
            if remark:
                current_entry['remark'] += remark
            # 追加原始备注用于验证
            if not pd.isna(original_remark):
                current_entry['original_remark_parts'].append(original_remark)
            # 更新原始文本
            current_entry['all_original_text'] += ' ' + str(original_industry_codes) + ' ' + str(original_remark)
        
        # 处理新子项或当前子项不存在的情况
        if is_new_entry or not current_entry:
            print(f"   处理新子项或当前子项不存在的情况")
            # 如果有当前子项，先处理它（实时生成JSON）
            if current_entry:
                print(f"   先处理当前子项（实时生成JSON）")
                process_current_entry(current_entry, result)
            
            # 创建新子项
            print(f"   创建新子项")
            current_entry = {
                'category_id': current_category['category_id'] if current_category else '',
                'category_name': current_category['category_name'] if current_category else '',
                'industry_name': industry_name,
                'standard': standard,
                'remark': remark,
                'original_industry_codes': original_industry_codes,
                'original_remark_parts': [original_remark] if not pd.isna(original_remark) else [],
                'original_contribution': original_contribution,
                'all_original_text': str(original_industry_codes) + ' ' + str(original_remark)
            }
    
    # 处理最后一个子项
    if current_entry:
        print(f"\n=== 处理最后一个子项 ===")
        print(f"   最后一个子项的category_id: {current_entry['category_id']}")
        print(f"   最后一个子项的industry_name: {current_entry['industry_name']}")
        process_current_entry(current_entry, result)
    
    # 检查0311中是否有2.2.7
    print(f"\n=== 检查最终结果 ===")
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

if __name__ == "__main__":
    main()

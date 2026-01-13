import pandas as pd
import re
import json

def debug_227_processing():
    # 读取Excel文件
    df = pd.read_excel('../src/green_finance_2025.xlsx', sheet_name=0, header=None)
    
    print("=== 调试2.2.7行的处理过程 ===")
    
    # 查找2.2.7行
    target_idx = None
    for idx, row in df.iterrows():
        category = str(row.iloc[0]).strip() if not pd.isna(row.iloc[0]) else ''
        if re.match(r'^2\.2\.7', category):
            target_idx = idx
            break
    
    if target_idx is None:
        print("❌ 未找到2.2.7行")
        return
    
    print(f"找到2.2.7行，索引为{target_idx}（行号{target_idx+1}）")
    
    # 处理2.2.7行，模拟convert_excel_to_json中的处理逻辑
    row = df.iloc[target_idx]
    
    # 获取原始行数据
    original_category = row.iloc[0]  # A列：领域
    original_industry_codes = row.iloc[1]  # B列：行业代码
    original_industry_name = row.iloc[2]  # C列：行业名称
    original_standard = row.iloc[3]  # D列：条件/标准
    original_remark = row.iloc[4]  # E列：备注
    original_contribution = row.iloc[5]  # F列：温室气体减排标识
    
    print(f"\n1. 原始行数据：")
    print(f"   A列（原始）: {repr(original_category)}")
    print(f"   B列（原始）: {repr(original_industry_codes)}")
    print(f"   C列（原始）: {repr(original_industry_name)}")
    print(f"   E列（原始）: {repr(original_remark[:100])}...")
    
    # 清洗当前行数据
    category_text = str(original_category) if not pd.isna(original_category) else ""
    industry_name = clean_text(original_industry_name, remove_hanzi_spaces=True)
    standard = clean_text(original_standard)
    remark = clean_text(original_remark)
    
    print(f"\n2. 清洗后的数据：")
    print(f"   A列（清洗）: {repr(category_text)}")
    print(f"   B列（清洗）: {repr(str(original_industry_codes).strip())}")
    print(f"   C列（清洗）: {repr(industry_name)}")
    print(f"   E列（清洗）: {repr(remark[:100])}...")
    
    # 检查是否是新的三级ID大分类（x.y.z格式）
    is_new_category = False
    new_category = None
    
    if category_text.strip():
        print(f"\n3. 处理category_text：")
        print(f"   category_text.strip(): {repr(category_text.strip())}")
        
        # 先清理干扰字符和多余空格，强化ID捕获
        cleaned_text = re.sub(r'[^\d\.\s\u4e00-\u9fa5]', '', category_text)
        print(f"   cleaned_text: {repr(cleaned_text)}")
        
        # 压缩连续空格
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        print(f"   cleaned_text（压缩空格）: {repr(cleaned_text)}")
        
        # 使用match从开头匹配，确保正确提取ID和名称
        match = re.match(r'([\d\.]+)\s+(.*)', cleaned_text)
        print(f"   match对象: {match}")
        
        if match:
            category_id = match.group(1)
            category_name = match.group(2)
            print(f"   match.group(1) (category_id): {repr(category_id)}")
            print(f"   match.group(2) (category_name): {repr(category_name)}")
        else:
            # 尝试手动分割
            space_pos = cleaned_text.find(' ')
            print(f"   手动分割的space_pos: {space_pos}")
            if space_pos != -1:
                category_id = cleaned_text[:space_pos]
                category_name = cleaned_text[space_pos+1:]
                print(f"   手动分割的category_id: {repr(category_id)}")
                print(f"   手动分割的category_name: {repr(category_name)}")
            else:
                category_id = cleaned_text
                category_name = ""
        
        # 清洗结果
        category_id = clean_text(category_id).replace(' ', '')
        category_name = clean_text(category_name, remove_hanzi_spaces=True)
        print(f"   最终category_id: {repr(category_id)}")
        print(f"   最终category_name: {repr(category_name)}")
        
        # 检查是否是三级ID
        print(f"   三级ID检查 (re.search(r'\d+\.\d+\.\d+', category_id)): {re.search(r'\d+\.\d+\.\d+', category_id)}")
        if re.search(r'\d+\.\d+\.\d+', category_id):
            new_category = {
                'category_id': category_id,
                'category_name': category_name
            }
            is_new_category = True
            print(f"   是新的三级分类: {is_new_category}")
            print(f"   new_category: {new_category}")
    
    print(f"\n4. 检查子项创建条件：")
    # 处理新的大分类
    current_category = new_category if is_new_category else None
    current_entry = None
    
    if is_new_category:
        # 新分类开启时，强制创建一个新子项来捕获首行内容
        force_new_entry = True
        print(f"   is_new_category=True，设置force_new_entry=True")
    else:
        force_new_entry = False
        print(f"   is_new_category=False，设置force_new_entry=False")
    
    # 检查是否是新子项（B列或C列不为空）
    has_industry_code = not pd.isna(original_industry_codes) and str(original_industry_codes).strip() not in ['', '-']
    has_industry_name = industry_name.strip() != ''
    is_new_entry = has_industry_code or has_industry_name or force_new_entry
    
    print(f"   has_industry_code (B列不为空且不是'-'): {has_industry_code}")
    print(f"   has_industry_name (C列不为空): {has_industry_name}")
    print(f"   is_new_entry (has_industry_code or has_industry_name or force_new_entry): {is_new_entry}")
    
    # 处理新子项或当前子项不存在的情况
    if is_new_entry or not current_entry:
        print(f"   is_new_entry or not current_entry: True，创建新子项")
        # 创建新子项
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
        print(f"   创建的current_entry: {json.dumps(current_entry, ensure_ascii=False, indent=2)}")
    
    print(f"\n5. 从E列提取代码：")
    # 从E列（备注）提取代码
    all_remarks = ""
    for original_remark_part in current_entry['original_remark_parts']:
        all_remarks += str(original_remark_part) + ' '
    if all_remarks:
        # 放宽提取正则：匹配3-4位数字，并使用单词边界确保完整匹配
        codes_from_e = re.findall(r'\b\d{3,4}\b', all_remarks)
        # 统一补全为4位数字
        codes_from_e = [code.zfill(4) for code in codes_from_e]
        print(f"   从E列提取的代码: {codes_from_e}")


def clean_text(text, remove_hanzi_spaces=False):
    """
    通用文本清洗函数
    :param text: 要清洗的文本
    :param remove_hanzi_spaces: 是否移除汉字间的空格
    :return: 清洗后的文本
    """
    if pd.isna(text) or text is None:
        return ""
    
    text = str(text)
    
    # 1. 将换行符替换为单个空格
    text = text.replace('\n', ' ')
    
    # 2. 移除汉字间的空格（如果需要）
    if remove_hanzi_spaces:
        # 使用正则表达式：如果空格的前后都是汉字，则将其删除
        text = re.sub(r'(?<=[\u4e00-\u9fa5])\s+(?=[\u4e00-\u9fa5])', '', text)
    
    # 3. 压缩连续的空格
    text = re.sub(r'\s+', ' ', text)
    
    # 4. 去除首尾空格
    text = text.strip()
    
    return text

if __name__ == "__main__":
    debug_227_processing()

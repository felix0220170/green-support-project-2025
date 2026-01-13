# 这个文件是将green_finance_2025.xlsx转换为green_finance_2025.json
import pandas as pd
import json
import re
import openpyxl
import os


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


def convert_excel_to_json():
    """
    智能子项识别算法：从大块聚合转向实时子项处理
    1. A列x.y.z作为大分类起始
    2. B列或C列不为空时启动新子项
    3. A、B、C同时为空时追加文本
    4. 实时生成JSON对象，不再全局join
    """
    # Step 1: 使用openpyxl引擎读取Excel文件，确保完整读取长文本
    print("正在读取Excel文件...")
    df = pd.read_excel('green_finance_2025.xlsx', sheet_name=0, header=None, engine='openpyxl')
    
    # Step 2: 初始化结果字典、当前分类上下文和当前子项
    result = {}
    current_category = None  # 当前大分类
    current_entry = None     # 当前处理的子项
    
    print("正在执行智能子项识别处理...")
    
    # 遍历所有行
    print(f"\n=== 开始遍历Excel行 ===")
    print(f"Excel文件总行数: {len(df)}")
    row_count = 0
    new_entry_count = 0
    
    for idx, row in df.iterrows():
        row_count += 1
        
        # 打印每一行的处理信息，方便追踪
        if idx >= 215 and idx <= 225:  # 只打印2.2.4到2.3.1之间的行
            print(f"\n=== 处理行（索引{idx}，行号{row_count}） ===")
            print(f"   A列内容: {repr(row.iloc[0])}")
        
        if row_count % 50 == 0:  # 每50行打印一次进度
            print(f"   已处理 {row_count} 行...")
        
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
        
        # 直接检查原始A列内容是否包含2.2.7
        if isinstance(original_category, str) and '2.2.7' in original_category:
            print(f"\n=== 找到2.2.7行（索引{idx}，行号{row_count}） ===")
            print(f"   原始A列内容: {repr(original_category)}")
            print(f"   类型: {type(original_category)}")
            # 尝试不同的方法来检查2.2.7是否存在
            print(f"   '2.2.7' in original_category: {'2.2.7' in original_category}")
            print(f"   '2.2' in original_category: {'2.2' in original_category}")
            print(f"   '7' in original_category: {'7' in original_category}")
            # 尝试转换为字符串并检查
            str_category = str(original_category)
            print(f"   转换为字符串后: {repr(str_category)}")
            print(f"   '2.2.7' in str_category: {'2.2.7' in str_category}")
        
        if is_target_row:
            print(f"   原始行数据:")
            print(f"      A列: {repr(original_category)}")
            print(f"      B列: {repr(original_industry_codes)}")
            print(f"      C列: {repr(original_industry_name)}")
            print(f"      D列: {repr(original_standard[:50] if not pd.isna(original_standard) else '')}...")
            print(f"      E列: {repr(original_remark[:50] if not pd.isna(original_remark) else '')}...")
        
        # 调试：检查前几行的数据
        if row_count <= 5:
            print(f"\n调试：处理第 {row_count} 行")
            print(f"   A列: {repr(original_category)}")
            print(f"   B列: {repr(original_industry_codes)}")
            print(f"   C列: {repr(original_industry_name)}")
        
        # 清洗当前行数据
        category_text = str(original_category) if not pd.isna(original_category) else ""
        industry_name = clean_text(original_industry_name, remove_hanzi_spaces=True)
        standard = clean_text(original_standard)
        remark = clean_text(original_remark)
        
        # 特别处理2.2.7行
        is_target_row = '2.2.7' in category_text
        if is_target_row:
            print(f"\n=== 处理目标行2.2.7（索引{idx}，行号{row_count}） ===")
            print(f"   清洗后的数据:")
            print(f"      category_text: {repr(category_text)}")
            print(f"      industry_name: {repr(industry_name)}")
            print(f"      standard: {repr(standard[:50])}...")
            print(f"      remark: {repr(remark[:50])}...")
            print(f"   原始行数据:")
            print(f"      A列: {repr(original_category)}")
            print(f"      B列: {repr(original_industry_codes)}")
            print(f"      C列: {repr(original_industry_name)}")
            print(f"      D列: {repr(original_standard[:50] if not pd.isna(original_standard) else '')}...")
            print(f"      E列: {repr(original_remark[:50] if not pd.isna(original_remark) else '')}...")
        
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
            # 如果有当前子项，先处理它（实时生成JSON）
            if current_entry:
                process_current_entry(current_entry, result)
                print(f"   调试：处理完当前子项，准备开始新分类")
            
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
    
        # 调试：检查2.2.7行的处理
        if category_text.strip() and '2.2.7' in category_text:
            print(f"\n调试：处理2.2.7行")
            print(f"   行号: {idx+1}")
            print(f"   category_text: {repr(category_text)}")
            print(f"   has_industry_code: {has_industry_code}")
            print(f"   has_industry_name: {has_industry_name}")
            print(f"   force_new_entry: {force_new_entry}")
            print(f"   is_new_entry: {is_new_entry}")
            print(f"   current_entry: {current_entry}")
        # 调试：检查2.2.7行之后的行
        elif current_entry and current_entry['category_id'] == '2.2.7':
            print(f"\n调试：处理2.2.7行之后的行")
            print(f"   行号: {idx+1}")
            print(f"   A列内容: {repr(category_text)}")
            print(f"   B列内容: {repr(original_industry_codes)}")
            print(f"   C列内容: {repr(original_industry_name)}")
            print(f"   current_entry的category_id: {current_entry['category_id']}")
        
        # 处理A、B、C同时为空的情况 - 追加到上一个子项
        a_b_c_empty = not category_text.strip() and not has_industry_code and not has_industry_name
        if a_b_c_empty and current_entry:
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
            # 如果有当前子项，先处理它（实时生成JSON）
            if current_entry:
                process_current_entry(current_entry, result)
            
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
    
    # 处理最后一个子项
    if current_entry:
        print(f"\n=== 主循环结束，处理最后一个子项 ===")
        print(f"最后一个子项的category_id: {current_entry['category_id']}")
        print(f"最后一个子项的industry_name: {current_entry['industry_name']}")
        process_current_entry(current_entry, result)
    else:
        print(f"\n=== 主循环结束，没有发现需要处理的最后一个子项 ===")

    # Step 4: 自动化冒烟测试
    print("正在执行自动化冒烟测试...")
    
    # 检查0311是否错误出现在5.1.10和5.1.12中
    for code in result:
        for item in result[code]:
            if code == "0311" and item["categoryId"] in ["5.1.10", "5.1.12"]:
                raise AssertionError(f"冒烟测试失败：代码 {code} 错误出现在分类 {item['categoryId']} 中")
    
    print("✅ 自动化冒烟测试通过")
    
    # Step 5: 保存为JSON文件
    output_file = 'output/green_finance_2025.json'
    
    # 确保output目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"JSON文件生成完成：{output_file}")
    return result


def process_current_entry(entry, result):
    """
    处理当前子项：
    1. 从原始数据中提取代码
    2. 确定代码来源（B列或E列）
    3. 生成JSON对象
    """
    # 转换减排贡献为数字
    if pd.isna(entry['original_contribution']) or entry['original_contribution'] == '':
        contribution_level = 0
    elif entry['original_contribution'] == '√':
        contribution_level = 1
    elif entry['original_contribution'] == '√√':
        contribution_level = 2
    else:
        contribution_level = 0
    
    # 调试2.2.7行的处理
    if entry['category_id'] == '2.2.7':
        print(f"\n=== 调试2.2.7行的process_current_entry函数 ===")
        print(f"   category_id: {entry['category_id']}")
        print(f"   category_name: {entry['category_name']}")
        print(f"   industry_name: {entry['industry_name']}")
    
    # 分别从B列和E列提取代码
    codes_from_b = []
    codes_from_e = []
    
    # 从B列（行业代码）提取
    industry_codes_str = str(entry['original_industry_codes']).strip()
    if industry_codes_str and industry_codes_str != "-":
        if ',' in industry_codes_str:
            codes_from_b = [code.strip().zfill(4) for code in industry_codes_str.split(',')]
        else:
            if re.match(r'^\d+$', industry_codes_str):
                # 补全为4位数字
                codes_from_b.append(industry_codes_str.zfill(4))
    
    # 从E列（备注）提取
    all_remarks = ""
    for original_remark in entry['original_remark_parts']:
        all_remarks += str(original_remark) + ' '
    
    if entry['category_id'] == '2.2.7':
        print(f"   original_remark_parts数量: {len(entry['original_remark_parts'])}")
        if entry['original_remark_parts']:
            print(f"   第一个original_remark_parts内容: {repr(entry['original_remark_parts'][0][:50])}...")
            print(f"   拼接后的all_remarks: {repr(all_remarks[:100])}...")
    
    if all_remarks:
        # 放宽提取正则：匹配3-4位数字，使用负向前瞻和负向后顾确保前后不是数字
        codes_from_e = re.findall(r'(?<![\d])\d{3,4}(?![\d])', all_remarks)
        # 统一补全为4位数字
        codes_from_e = [code.zfill(4) for code in codes_from_e]
        
        if entry['category_id'] == '2.2.7':
            print(f"   从E列提取的代码: {codes_from_e}")
            print(f"   包含0311: {'0311' in codes_from_e}")
    
    # 处理B列代码
    for code in codes_from_b:
        if len(code) == 4:
            # 只要正则在这一块逻辑区域内抓到了数字，就信任它，不再进行二次检查
            if code not in result:
                result[code] = []
            result[code].append({
                "categoryId": entry['category_id'],
                "categoryName": entry['category_name'],
                "industryName": entry['industry_name'],
                "standard": entry['standard'],
                "remark": entry['remark'],
                "contribution_level": contribution_level,
                "matchSource": "industry_column"
            })
    
    # 处理E列代码
    for code in codes_from_e:
        if len(code) == 4:
            # 只要正则在这一块逻辑区域内抓到了数字，就信任它，不再进行二次检查
            if code not in result:
                result[code] = []
            if entry['category_id'] == '2.2.7' and code == '0311':
                print(f"   调试：将2.2.7的子项添加到代码0311中")
                print(f"      categoryId: {entry['category_id']}")
                print(f"      categoryName: {entry['category_name']}")
                print(f"      industryName: {entry['industry_name']}")
            result[code].append({
                "categoryId": entry['category_id'],
                "categoryName": entry['category_name'],
                "industryName": entry['industry_name'],
                "standard": entry['standard'],
                "remark": entry['remark'],
                "contribution_level": contribution_level,
                "matchSource": "remark_column"
            })



def verify_data(data):
    """
    内建自动化"边缘案例"自检
    """
    print("\n=== 自动化数据校验开始 ===")
    
    # 1. 打印代码 3411 对应的所有对象的 categoryId 和 categoryName
    print("\n1. 代码 3411 对应的所有对象的 categoryId 和 categoryName：")
    if "3411" in data:
        for i, project in enumerate(data["3411"]):
            print(f"   项目 {i+1}: categoryId={project['categoryId']}, categoryName={project['categoryName']}")
    else:
        print("   ❌ 代码 3411 不存在")
    
    # 2. 打印代码 3521 的 remark 字段
    print("\n2. 代码 3521 的 remark 字段内容：")
    if "3521" in data:
        for project in data["3521"]:
            if project["categoryId"] == "1.1.1":
                print(f"   categoryId=1.1.1 的 remark 内容：")
                print(f"   {project['remark'][:200]}..." if len(project['remark']) > 200 else f"   {project['remark']}")
                print(f"   remark 长度: {len(project['remark'])} 个字符")
                break
    else:
        print("   ❌ 代码 3521 不存在")
    
    # 3. 统计 contribution_level 为 1 和 2 的项目数量
    print("\n3. 减排贡献等级统计：")
    level_counts = {0: 0, 1: 0, 2: 0}
    for code, projects in data.items():
        for project in projects:
            level = project["contribution_level"]
            if level in level_counts:
                level_counts[level] += 1
    
    print(f"   contribution_level=1 (低碳赋能) 的项目数量: {level_counts[1]}")
    print(f"   contribution_level=2 (直接减排) 的项目数量: {level_counts[2]}")
    print(f"   contribution_level=0 (无标识) 的项目数量: {level_counts[0]}")
    
    # 4. 内建自动化"边缘案例"自检
    print("\n4. 内建自动化边缘案例自检：")
    
    # Case 2.4.3: 检查 Key "0190" 必须出现在 categoryId: "2.4.3" 下，且其 remark 必须包含完整的行业列表，直到 "0181 草种植" 为止，严禁截断
    print("   案例 2.4.3 检查：")
    if "0190" in data:
        found = False
        for project in data["0190"]:
            if project["categoryId"] == "2.4.3":
                found = True
                remark = project["remark"]
                # 检查remark是否包含"0181 草种植"（这是完整性的关键标志）
                if "0181 草种植" in remark:
                    print("   ✅ 代码 0190 在 categoryId: 2.4.3 下的 remark 包含完整列表")
                    print(f"      remark 长度: {len(remark)} 个字符")
                    # 输出remark结尾部分以验证
                    print(f"      remark 结尾: {remark[-50:]}")
                else:
                    print("   ❌ 错误：代码 0190 在 categoryId: 2.4.3 下的 remark 不包含 '0181 草种植'，可能被截断")
                    print(f"      remark 内容: {remark}")
                break
        if not found:
            print("   ❌ 错误：代码 0190 不包含 categoryId: 2.4.3")
    else:
        print("   ❌ 错误：代码 0190 不存在")
    
    # Case 5.1.11: 检查 Key "0111" 在 categoryId: "5.1.11" 下的 remark 是否以 "符合本条目规定条件的农作物种植活动" 结尾
    print("   案例 5.1.11 检查：")
    if "0111" in data:
        found = False
        for project in data["0111"]:
            if project["categoryId"] == "5.1.11":
                found = True
                remark = project["remark"]
                # 检查remark是否以"符合本条目规定条件的农作物种植活动"结尾（忽略空格差异）
                normalized_remark = re.sub(r'\s+', '', remark.strip())
                # 添加调试信息
                print(f"      原始remark结尾: {remark[-50:]}")
                print(f"      标准化后结尾: {normalized_remark[-20:]}")
                if normalized_remark.endswith("符合本条目规定条件的农作物种植活动") or normalized_remark.endswith("符合本条目规定条件的农作物种植活动。"):
                    print("   ✅ 代码 0111 在 categoryId: 5.1.11 下的 remark 格式正确，未被截断")
                    print(f"      remark 结尾: {remark[-50:]}")
                elif normalized_remark.endswith("0142食用菌") or normalized_remark.endswith("0142食用菌种植") or normalized_remark.endswith("0142食用菌种植活动"):
                    print("   ❌ 错误：代码 0111 在 categoryId: 5.1.11 下的 remark 以 '0142 食用菌' 结尾，判定为读取截断错误")
                    print(f"      remark 结尾: {remark[-50:]}")
                else:
                    print("   ⚠️ 警告：代码 0111 在 categoryId: 5.1.11 下的 remark 既不以 '符合本条目规定条件的农作物种植活动' 结尾，也不以 '0142 食用菌' 结尾")
                    print(f"      remark 结尾: {remark[-50:]}")
                break
        if not found:
            print("   ❌ 错误：代码 0111 不包含 categoryId: 5.1.11")
    else:
        print("   ❌ 错误：代码 0111 不存在")
    
    # Case 5.1.3: 检查 Key "0190" 是否正确映射到 categoryId: "5.1.3" (绿色农业生产)
    print("   案例 5.1.3 检查：")
    if "0190" in data:
        found = False
        for project in data["0190"]:
            if project["categoryId"] == "5.1.3" and project["categoryName"] == "绿色农业生产":
                found = True
                print("   ✅ 代码 0190 正确映射到 categoryId: 5.1.3 (绿色农业生产)")
                break
        if not found:
            print("   ❌ 错误：代码 0190 未正确映射到 categoryId: 5.1.3 (绿色农业生产)")
    else:
        print("   ❌ 错误：代码 0190 不存在")
    
    # 5. 新的校验案例（根据用户要求）
    print("\n5. 新的校验案例：")
    
    # Case 0311: 打印所有关联的 categoryId
    print("   案例 0311 检查：")
    if "0311" in data:
        print("   代码 0311 关联的所有 categoryId：")
        for i, project in enumerate(data["0311"]):
            print(f"   项目 {i+1}: categoryId={project['categoryId']}, categoryName={project['categoryName']}")
    else:
        print("   ❌ 错误：代码 0311 不存在")
    
    # Case 0111: 必须关联到 2.4.3，禁止关联到 2.5
    print("   案例 0111 检查：")
    if "0111" in data:
        found_243 = False
        found_25 = False
        for project in data["0111"]:
            if project["categoryId"] == "2.4.3":
                found_243 = True
            if project["categoryId"] == "2.5":
                found_25 = True
        
        if found_243:
            print("   ✅ 代码 0111 正确关联到 categoryId: 2.4.3")
        else:
            print("   ❌ 错误：代码 0111 未关联到 categoryId: 2.4.3")
        
        if found_25:
            print("   ❌ 错误：代码 0111 关联到了禁止的 categoryId: 2.5")
        else:
            print("   ✅ 代码 0111 未关联到禁止的 categoryId: 2.5")
    else:
        print("   ❌ 错误：代码 0111 不存在")
    
    print("\n=== 自动化数据校验结束 ===")


if __name__ == "__main__":
    # 执行转换
    data = convert_excel_to_json()
    
    # 执行验证
    verify_data(data)
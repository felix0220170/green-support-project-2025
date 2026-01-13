import json
import os

# 定义文件路径
INPUT_FILE = 'output/parsed_excel_rows.json'
OUTPUT_FILE = 'output/two_level_structure.json'

# 创建输出目录
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

def process_data():
    """
    将平铺的数据转换为两层结构：
    - 父元素：A列中以1.1.1这样开头的值
    - 子元素：B, C, D, E, F作为属性
    """
    # 读取解析后的数据
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        parsed_rows = json.load(f)
    
    print(f"共读取了 {len(parsed_rows)} 行数据")
    
    # 处理数据
    processed_data = []
    current_parent = None
    category_map = {}  # 用于跟踪已创建的父元素，避免重复
    
    for row in parsed_rows:
        # 忽略特定行
        row_num = row['row_num']
        if row_num in [1, 2]:  # 忽略标题行和列头行
            continue
        
        # 获取A列值并清理
        a_value = str(row['A']).strip() if row['A'] is not None else ''
        
        # 检查是否是有效的父元素（以数字+点开头，如1.1.1）
        import re
        is_valid_parent = False
        special_case = False
        
        if a_value:
            # 检查是否以数字+点+数字+点+数字开头
            if re.match(r'^\d+\.\d+\.\d+', a_value):
                is_valid_parent = True
            elif a_value in ['设备制造', '备制造'] and current_parent:
                # 特殊处理：将"设备制造"或"备制造"与上一行的父元素合并
                # 检查父元素名称是否已经包含完整的名称，避免重复合并
                if not current_parent['category_name'].endswith('设备制造') and not current_parent['category_name'].endswith('备制造'):
                    current_parent['category_name'] += a_value
                    # 更新category_map中的父元素引用
                    category_map[current_parent['category_id']] = current_parent
                # 对于"备制造"这样的特殊情况，不要跳过，让它作为子元素添加
                if a_value == '备制造':
                    special_case = False
                else:
                    special_case = True
            elif a_value in ['制造'] and current_parent:
                # 处理类似"1.1.17 余热余压余气利用设" + "备制造"的情况
                if current_parent['category_name'].endswith('设'):
                    current_parent['category_name'] = current_parent['category_name'].rstrip('设') + '设备制造'
                    # 更新category_map中的父元素引用
                    category_map[current_parent['category_id']] = current_parent
                special_case = True
        
        # 如果是特殊情况，继续处理下一行
        if special_case:
            continue
        
        # 如果是新的有效父元素
        if is_valid_parent:
            # 清理category_name（移除换行符和多余空格）
            category_name = a_value.replace('\n', '').strip()
            # 处理可能的多余空格（只保留1.1.1后面的一个空格）
            category_name = re.sub(r'\s+', ' ', category_name)
            
            # 提取category_id
            category_id = category_name.split()[0] if category_name.split() else ''
            
            # 检查是否已存在该category_id的父元素
            if category_id in category_map:
                # 如果已存在，使用现有父元素
                current_parent = category_map[category_id]
            else:
                # 创建新的父元素
                current_parent = {
                    'category_id': category_id,
                    'category_name': category_name,
                    'children': []
                }
                processed_data.append(current_parent)
                category_map[category_id] = current_parent
        
        # 如果A列为空，使用当前父元素（如果有的话）
        elif a_value == '':
            # 如果没有当前父元素，跳过
            if current_parent is None:
                continue
        
        # 如果不是有效的父元素且不是"1."或"1.1"这样的章节标题
        elif a_value and (a_value.startswith('1.') and not re.match(r'^\d+\.\d+\.\d+', a_value)):
            # 忽略章节标题行
            continue
        
        # 处理父元素不完整的情况（如行62和行63的情况）
        elif a_value and not is_valid_parent and current_parent and current_parent['category_name'].endswith('设'):
            # 将当前a_value与父元素合并
            # 检查父元素名称是否已经包含完整的名称，避免重复合并
            if not current_parent['category_name'].endswith('设备制造') and not current_parent['category_name'].endswith('备制造'):
                current_parent['category_name'] += a_value
                # 更新category_map中的父元素引用
                category_map[current_parent['category_id']] = current_parent
            continue
        
        # 如果有current_parent，则将当前行作为子元素添加
        if current_parent is not None:
            # 创建子元素
            child = {
                'B': row['B'],
                'C': row['C'],
                'D': row['D'],
                'E': row['E'],
                'F': row['F'],
                'row_num': row['row_num']
            }
            current_parent['children'].append(child)
    
    # 保存处理后的数据
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n处理完成！")
    print(f"处理后的数据已保存到: {OUTPUT_FILE}")
    
    # 统计信息
    print(f"\n数据统计:")
    print(f"  父元素数量: {len(processed_data)}")
    total_children = sum(len(parent['children']) for parent in processed_data)
    print(f"  子元素总数量: {total_children}")
    
    # 打印前几个父元素的信息
    print(f"\n前5个父元素信息:")
    for i, parent in enumerate(processed_data[:5]):
        print(f"  {i+1}. {parent['category_name']} (子元素数量: {len(parent['children'])})")
    
    return processed_data

if __name__ == "__main__":
    processed_data = process_data()
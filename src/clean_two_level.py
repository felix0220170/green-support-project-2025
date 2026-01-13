import json
import os

# 定义文件路径
INPUT_FILE = 'output/modified_two_level_structure.json'
OUTPUT_FILE = 'output/cleaned_two_level_structure.json'

def clean_two_level_data():
    """
    清理两层结构数据：
    1. 移除所有B='0000'且C=None的子元素
    2. 移除所有B='0000'且C=None且D列内容与前一个子元素D列内容重复的子元素
    """
    # 读取原始数据
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 处理数据
    for parent in data:
        # 保留有效的子元素
        valid_children = []
        prev_child = None
        
        for child in parent['children']:
            # 检查是否是无效的子元素
            is_invalid = False
            # 情况1：B='0000'且C=None
            if child['B'] == '0000' and child['C'] is None:
                is_invalid = True
            # 情况2：B='0000'且C和D内容相同（章节标题行）
            elif child['B'] == '0000' and child['C'] and child['D']:
                if child['C'] == child['D']:
                    # 进一步检查是否是章节标题格式（如"4.能源绿色低碳转型"）
                    is_invalid = True
            # 情况3：可能是其他类型的无效条目
            elif child['B'] == '0000' and (child['C'] is None or child['D'] is None):
                is_invalid = True
            
            # 检查是否与前一个子元素的D列内容重复
            is_duplicate = False
            if prev_child and child['D'] and prev_child['D']:
                # 内容相同但B或C不同时，不视为重复
                # 这些通常是不同行业代码但适用相同标准的情况
                if child['D'] == prev_child['D']:
                    # 只有当B和C都相同时才视为重复
                    if child['B'] == prev_child['B'] and child['C'] == prev_child['C']:
                        is_duplicate = True
                # 对于内容包含的情况，保持更严格的检查
                elif len(child['D']) > len(prev_child['D']) and prev_child['D'] in child['D']:
                    # 只有当B或C相同时才可能是真正的重复
                    if child['B'] == prev_child['B'] or child['C'] == prev_child['C']:
                        is_duplicate = True
            
            # 如果不是无效的子元素且不是重复的内容，则保留
            if not is_invalid and not is_duplicate:
                valid_children.append(child)
                prev_child = child
        
        # 更新父元素的子元素列表
        parent['children'] = valid_children
    
    # 保存清理后的数据
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"清理完成！")
    print(f"清理后的数据已保存到: {OUTPUT_FILE}")
    
    # 统计信息
    total_children = sum(len(parent['children']) for parent in data)
    print(f"\n数据统计:")
    print(f"  父元素数量: {len(data)}")
    print(f"  子元素总数量: {total_children}")

if __name__ == "__main__":
    clean_two_level_data()

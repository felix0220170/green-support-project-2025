import json
import os
import re

# 定义文件路径
INPUT_FILE = 'output/final_two_level_structure.json'
OUTPUT_FILE = 'output/final_two_level_structure_cleaned.json'

def remove_newlines_and_spaces_from_category():
    """
    去除所有父元素的category_name中的换行符和不应该存在的空格
    """
    # 读取原始数据
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 统计处理的category_name数量
    processed_count = 0
    
    # 处理数据
    for parent in data:
        category_name = parent['category_name']
        original_name = category_name
        
        # 去除换行符
        if '\n' in category_name:
            category_name = category_name.replace('\n', '')
        
        # 去除单词之间不应该存在的空格（保留中文标点符号前后的空格）
        # 使用正则表达式匹配中文字符之间的空格
        if ' ' in category_name:
            # 匹配两个中文字符之间的单个空格并去除
            category_name = re.sub(r'([\u4e00-\u9fa5])\s+([\u4e00-\u9fa5])', r'\1\2', category_name)
        
        # 如果有修改，更新category_name
        if category_name != original_name:
            processed_count += 1
            parent['category_name'] = category_name
    
    # 保存修改后的数据
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"修改完成！")
    print(f"共处理了 {processed_count} 个category_name")
    print(f"修改后的数据已保存到: {OUTPUT_FILE}")
    
    # 统计信息和示例
    print(f"\n数据统计:")
    print(f"  父元素数量: {len(data)}")
    print(f"  子元素总数量: {sum(len(parent['children']) for parent in data)}")
    
    # 检查是否还有包含问题的category_name
    remaining_issues = sum(1 for parent in data if '\n' in parent['category_name'] or re.search(r'([\u4e00-\u9fa5])\s+([\u4e00-\u9fa5])', parent['category_name']))
    if remaining_issues == 0:
        print(f"\n✅ 所有category_name中的换行符和不应该存在的空格已成功去除")
    else:
        print(f"\n❌ 仍有 {remaining_issues} 个category_name包含问题")

if __name__ == "__main__":
    remove_newlines_and_spaces_from_category()

import re

# 测试文本
test_text = "包括但不限于 0311 牛的饲养、0312马的饲养、0313 猪的饲养、0314 羊的饲养、"

print(f"测试文本: {repr(test_text)}")
print()

# 测试当前的正则表达式
print(f"=== 测试当前正则表达式: r'\\b\\d{3,4}\\b' ===")
matches = re.findall(r'\b\d{3,4}\b', test_text)
print(f"匹配结果: {matches}")
print(f"包含0312: {'0312' in matches}")

# 测试每个代码的匹配情况
for code in ['0311', '0312', '0313', '0314']:
    match = re.search(r'\b' + code + r'\b', test_text)
    print(f"   {code} 匹配结果: {match}")
    if match:
        # 打印匹配位置和前后字符
        start = max(0, match.start() - 5)
        end = min(len(test_text), match.end() + 5)
        print(f"      上下文: '{test_text[start:end]}'")

print()

# 测试不同的正则表达式
print(f"=== 测试其他正则表达式 ===")

# 测试不使用单词边界的情况
pattern1 = r'\d{3,4}'
matches1 = re.findall(pattern1, test_text)
print(f"正则表达式 {repr(pattern1)} 匹配结果: {matches1}")
print(f"包含0312: {'0312' in matches1}")

# 测试改进的正则表达式，处理中文边界
pattern2 = r'(?<![\d])\d{3,4}(?![\d])'
matches2 = re.findall(pattern2, test_text)
print(f"正则表达式 {repr(pattern2)} 匹配结果: {matches2}")
print(f"包含0312: {'0312' in matches2}")

# 测试处理中文和数字边界
pattern3 = r'(?<!\w)\d{3,4}(?!\w)'
matches3 = re.findall(pattern3, test_text)
print(f"正则表达式 {repr(pattern3)} 匹配结果: {matches3}")
print(f"包含0312: {'0312' in matches3}")

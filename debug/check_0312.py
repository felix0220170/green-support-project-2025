import json

# 读取JSON文件
with open('../output/green_finance_2025.json', 'r', encoding='utf-8') as f:
    result = json.load(f)

print(f"=== 检查0312是否包含2.2.7 ===")

# 检查0312中是否有2.2.7
if '0312' in result:
    print(f"0312 中有 {len(result['0312'])} 个条目")
    found = False
    for item in result['0312']:
        if item['categoryId'] == '2.2.7':
            print(f"✅ 找到2.2.7在0312中")
            print(f"   categoryId: {item['categoryId']}")
            print(f"   categoryName: {item['categoryName']}")
            print(f"   industryName: {item['industryName']}")
            found = True
            break
    if not found:
        print(f"❌ 0312中没有2.2.7")
        print(f"0312中的所有categoryId:")
        for item in result['0312']:
            print(f"   - {item['categoryId']} ({item['categoryName']})")
else:
    print(f"❌ 0312不在JSON文件中")

print(f"\n=== 检查2.2.7的所有关联代码 ===")

# 查找所有关联到2.2.7的代码
codes_with_227 = []
for code, items in result.items():
    for item in items:
        if item['categoryId'] == '2.2.7':
            codes_with_227.append(code)
            break

print(f"关联到2.2.7的代码共有 {len(codes_with_227)} 个:")
for code in sorted(codes_with_227):
    print(f"   - {code}")

print(f"\n=== 检查E列中所有代码的提取情况 ===")

expected_codes = ['0311', '0312', '0313', '0314', '0315', '0319', '0321', '0322', '0323']
print(f"E列中应该提取的代码: {', '.join(expected_codes)}")
print(f"实际提取的代码: {', '.join(sorted(codes_with_227))}")

# 检查是否有遗漏的代码
missing_codes = [code for code in expected_codes if code not in codes_with_227]
if missing_codes:
    print(f"遗漏的代码: {', '.join(missing_codes)}")
else:
    print(f"✅ 所有代码都已正确提取")

from datetime import datetime, timedelta

def calculate_rules(dateStart, dateEnd, rootRules, calculateQuantity):
    # 定义一个结果列表
    result = []

    # 将字符串日期转换为 datetime 对象
    current_start = datetime.strptime(dateStart, "%Y-%m-%d")
    current_end = datetime.strptime(dateEnd, "%Y-%m-%d")

    # 每阶段周期为90天
    period_days = 90

    # 规则循环逻辑
    current_rules = rootRules[:]

    for _ in range(calculateQuantity):
        # 计算下一个阶段的开始和结束日期
        next_start = current_end + timedelta(days=1)
        next_end = next_start + timedelta(days=period_days)

        # 轮换规则：将最后一个移到第一个位置，其他元素后移
        next_rules = [current_rules[-1]] + current_rules[:-1]

        # 将阶段信息添加到结果中
        result.append([
            next_start.strftime("%Y-%m-%d"),
            next_end.strftime("%Y-%m-%d"),
            next_rules
        ])

        # 更新当前阶段的信息
        current_start = next_start
        current_end = next_end
        current_rules = next_rules

    return result

# 示例输入
dateStart = "2024-04-01"
dateEnd = "2024-06-30"
rootRules = ["5,0", "1,6", "2,7", "3,8", "4,9"]
calculateQuantity = 300

# 运行函数
output = calculate_rules(dateStart, dateEnd, rootRules, calculateQuantity)

# 写入结果到txt文件
with open('限行规则推算结果.txt', 'w', encoding='utf-8') as f:
    for phase in output:
        start_date, end_date, rule_list = phase
        f.write(f"阶段：{start_date} 至 {end_date}\n")
        for day_index, restricted_plates in enumerate(rule_list, start=1):
            weekday_map = {1: '周一', 2: '周二', 3: '周三', 4: '周四', 5: '周五', 6: '周六', 7: '周日'}
            f.write(f"  {weekday_map[day_index]}: 限行尾号 {restricted_plates}\n")
        f.write("\n")

print("结果已成功写入 '限行规则推算结果.txt' 文件")
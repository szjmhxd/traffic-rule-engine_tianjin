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

# 打印结果
print(output)
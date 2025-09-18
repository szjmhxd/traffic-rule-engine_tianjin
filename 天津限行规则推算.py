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
        result.append(
            [next_start.strftime("%Y-%m-%d"), next_end.strftime("%Y-%m-%d"), next_rules]
        )

        # 更新当前阶段的信息
        current_start = next_start
        current_end = next_end
        current_rules = next_rules

    return result


def filter_rules_by_date_range(all_rules, target_start_str, target_end_str):
    """
    从所有推算规则中筛选出指定时间段内的规则
    """
    # 将目标时间段转换为 datetime 对象
    target_start = datetime.strptime(target_start_str, "%Y-%m-%d")
    target_end = datetime.strptime(target_end_str, "%Y-%m-%d")

    filtered_rules = []

    # 遍历所有规则，筛选出与目标时间段有交集的规则
    for phase in all_rules:
        phase_start = datetime.strptime(phase[0], "%Y-%m-%d")
        phase_end = datetime.strptime(phase[1], "%Y-%m-%d")

        # 检查时间段是否有交集
        if phase_end >= target_start and phase_start <= target_end:
            # 计算实际有效的开始和结束日期
            effective_start = max(phase_start, target_start).strftime("%Y-%m-%d")
            effective_end = min(phase_end, target_end).strftime("%Y-%m-%d")

            # 对于完全在目标时间段内的阶段，保留全部信息
            if phase_start >= target_start and phase_end <= target_end:
                filtered_rules.append(phase)
            else:
                # 对于部分重叠的阶段，只记录有效的日期范围
                filtered_rules.append([effective_start, effective_end, phase[2]])

    return filtered_rules


# 示例输入 - 基础推算参数
dateStart = "2024-04-01"
dateEnd = "2024-06-30"
rootRules = ["5,0", "1,6", "2,7", "3,8", "4,9"]
calculateQuantity = 300

# 目标时间段 - 用户可以修改为需要的时间段
# target_start_date = "2025-01-01"
# target_end_date = "2026-12-31"

# # 通过input输入年份，计算整年时间范围
# input_year = input("请输入需要查询的年份（如：2025）：")
# target_start_date = f"{input_year}-01-01"
# target_end_date = f"{input_year}-12-31"

# 通过input输入起始年份和结束年份，计算多年份时间范围
input_years = input("请输入需要查询的年份范围（如：2022-2033）：")
start_year, end_year = input_years.split("-")
target_start_date = f"{start_year}-01-01"
target_end_date = f"{end_year}-12-31"

# 运行函数 - 先推算所有规则
all_output = calculate_rules(dateStart, dateEnd, rootRules, calculateQuantity)

# 筛选出目标时间段内的规则
filtered_output = filter_rules_by_date_range(
    all_output, target_start_date, target_end_date
)

# 写入筛选后的结果到txt文件
output_file = f"限行规则推算结果_{target_start_date}_{target_end_date}.txt"
with open(output_file, "w", encoding="utf-8") as f:
    for phase in filtered_output:
        start_date, end_date, rule_list = phase
        f.write(f"阶段：{start_date} 至 {end_date}\n")
        for day_index, restricted_plates in enumerate(rule_list, start=1):
            weekday_map = {
                1: "周一",
                2: "周二",
                3: "周三",
                4: "周四",
                5: "周五",
                6: "周六",
                7: "周日",
            }
            f.write(f"  {weekday_map[day_index]}: 限行尾号 {restricted_plates}\n")
        f.write("\n")

print(
    f"已成功推算并筛选 {target_start_date} 至 {target_end_date} 的限行规则，并写入 '{output_file}' 文件"
)
print(f"共筛选出 {len(filtered_output)} 个阶段的限行规则")

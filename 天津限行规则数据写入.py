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

def generate_insert_statements(region, rules):
    # 初始化 SQL 语句列表
    sql_statements = []

    # 遍历规则生成 INSERT 语句
    for phase in rules:
        start_date, end_date, rule_list = phase
        for day_of_week, restricted_plates in enumerate(rule_list, start=1):
            sql = (
                f"INSERT INTO `jy_traffic_restriction_rules` ("
                f"`region`, `start_date`, `end_date`, `day_of_week`, `restricted_plates`) "
                f"VALUES ("
                f"'{region}', '{start_date}', '{end_date}', {day_of_week}, '{restricted_plates}'); "
            )
            sql_statements.append(sql)

    return sql_statements

# 示例输入
# dateStart = "2024-04-01"
# dateEnd =   "2024-06-30"
# rootRules = ["5,0", "1,6", "2,7", "3,8", "4,9"]

dateStart = "2022-07-04"
dateEnd =   "2022-10-02"
rootRules = ['2,7', '3,8', '4,9', '5,0', '1,6']

calculateQuantity = 20 # 计算的阶段数量
region = "天津"

# 运行函数
rules = calculate_rules(dateStart, dateEnd, rootRules, calculateQuantity)
insert_statements = generate_insert_statements(region, rules)

# 打印 SQL 语句
for statement in insert_statements:
    print(statement)

def calculate_basic_metrics(target_users: str) -> str:
    """Return simple product metric formulas for downstream reasoning."""
    return f"""
# Metrics Tool Output

目标用户：{target_users}

建议使用这些基础指标公式：

- Activation Rate = 完成关键首次行为的用户数 / 新注册用户数
- D1 Retention = 次日回访用户数 / 当日新增用户数
- D7 Retention = 第 7 天仍活跃用户数 / 当日新增用户数
- Conversion Rate = 付费用户数 / 试用或注册用户数
- Task Completion Rate = 成功完成核心任务次数 / 发起核心任务次数
- North Star Metric 应该同时反映用户价值和业务增长
""".strip()

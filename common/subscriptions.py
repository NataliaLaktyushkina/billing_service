def get_subscription_intervals(subscription_name: str) -> tuple:
    if subscription_name=='month':
        interval = 'month'
        interval_count = 1
    elif subscription_name == 'three_months':
        interval = 'month'
        interval_count = 3
    elif subscription_name == 'year':
        interval = 'year'
        interval_count = 1
    return interval, interval_count

def daily_return(close):
    return (close / close.shift(1)) - 1


def cum_return(daily_return):
    return (1 + daily_return).cumprod()

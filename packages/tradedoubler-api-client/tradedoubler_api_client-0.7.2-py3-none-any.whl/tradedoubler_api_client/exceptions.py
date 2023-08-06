class TradedoublerConnectionError(ConnectionError):
    pass


class TradedoublerRateLimitExceeded(TradedoublerConnectionError):
    pass

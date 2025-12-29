from rest_framework.throttling import UserRateThrottle

class FifteenMinuteRateThrottle(UserRateThrottle):
    """
    Custom throttle to allow 100 requests per 15 minutes.
    """
    scope = 'user_15min'

    def parse_rate(self, rate):
        if not rate:
            return (None, None)
        
        # We expect a rate like '100/15m'
        num_requests, period = rate.split('/')
        num_requests = int(num_requests)
        
        if period.endswith('m'):
            minutes = int(period[:-1])
            return (num_requests, minutes * 60)
            
        return super().parse_rate(rate)

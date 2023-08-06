class TimeOutException(Exception):
    pass

def alarm_handler(signum, frame):
    raise TimeOutException("Database connection timeout has been reached")
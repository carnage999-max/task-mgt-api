import datetime
from datetime import timedelta


now = datetime.datetime.now()

sp_time = datetime.datetime(2005, 2, 22, 21)

if now and now > sp_time:
    print("damn")
    

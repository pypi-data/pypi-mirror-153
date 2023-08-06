### Timeout
Random timeout between minimum and maximum values

Installation:
`pip install python-timeout`

Usage:
```
from timeout import random_timeout, sleep_for

random_timeout(10, 20) # Random timeout between 10 and 20 seconds
random_timeout(from_minutes=1, to_minutes=2) # Random timeout between one and two minutes
random_timeout(from_hours=1, to_hours=2) # Random timeout between one and two hours
random_timeout(from_days=3, to_days=7) # Random timeout between one and two hours
random_timeout(1) # Random timeout for around one second
random_timeout(from_hours=1) # Random timeout for around one hour

sleep_for(5) # Sleep for five minutes
sleep_for(15) # Sleep for fifteen minutes
sleep_for(hours=2) # Sleep for two hours
```

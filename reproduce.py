import datetime
from django.utils.timesince import timesince

def test_long_interval_with_tz():
    now = datetime.datetime.now(datetime.timezone.utc)
    d = now - datetime.timedelta(days=31)
    print(timesince(d))

if __name__ == "__main__":
    test_long_interval_with_tz()

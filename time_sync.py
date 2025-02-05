import ntplib
from time import ctime, sleep

def sync_time(retries=5):
    for attempt in range(retries):
        try:
            client = ntplib.NTPClient()
            response = client.request('pool.ntp.org', version=3)
            print(f"Time synchronized: {ctime(response.tx_time)}")
            return True
        except Exception as e:
            print(f"Failed to synchronize time (attempt {attempt + 1}): {e}")
            sleep(2)  # Wait before retrying
    return False

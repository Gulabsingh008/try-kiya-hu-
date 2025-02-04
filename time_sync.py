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

def continuous_time_check():
    while True:
        if not sync_time():
            print("Failed to synchronize time. Retrying...")
        sleep(60)  # Check every minute

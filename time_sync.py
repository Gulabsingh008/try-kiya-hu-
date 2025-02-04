from time import ctime, sleep
import ntplib

def sync_time(retries=5):
    for attempt in range(retries):
        try:
            client = ntplib.NTPClient()
            # Replace the NTP server URL here
            response = client.request('time.google.com', version=3)  # Changed NTP server
            print(f"Time synchronized: {ctime(response.tx_time)}")
            return True
        except Exception as e:
            print(f"Failed to synchronize time (attempt {attempt + 1}): {e}")
            sleep(2)  # Wait before retrying
    return False

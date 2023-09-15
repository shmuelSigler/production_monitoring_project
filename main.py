import requests
import time
import json
import random
import os

# URL to monitor
url = "https://chargeflow.io"
instatus_api_key = "bf6b967c74e3067ecbf47e8c9a713cda"


def update_instatus(status):
    headers = {
        "Authorization": f"Bearer {instatus_api_key}",
        "Content-Type": "application/json",
    }

    data = {
        "status": status,
    }

    response = requests.put(
        f"https://api.instatus.com/v2/clmk8mhlx51086bbmxegve6cb3",
        headers=headers,
        data=json.dumps(data),
    )

    # print(response.json()["status"])
    return response.status_code


def monitor_website():
    try:
        response = requests.get(url)
        response.raise_for_status()     # Raise an exception for HTTP errors
        return "UP"
    except requests.exceptions.RequestException:
        return "HASISSUES"


def main():
    current_hour = time.localtime().tm_hour     # The hour (0-23)
    current_min = time.localtime().tm_min       # The minute (0-59)
    downtime = 0
    print(current_hour, current_min)
    # Load the previous downtime value from the workflow artifact
    previous_downtime = int(os.getenv("DOWNTIME", "0"))
    print(previous_downtime)

    # Simulate failures at specific times (2:00am, 4:00am, 6:00am)
    if previous_downtime < 10:
        if current_hour % 2 == 0 and current_min == 0:
            downtime = random.randint(5, 15)
            status = "HASISSUES"
        else:
            status = monitor_website()
    else:
        status = "HASISSUES"

    # Save the current downtime value as an artifact for the next run
    with open("downtime.txt", "w") as downtime_file:
        downtime_file.write(str(downtime))

    update_instatus(status)


if __name__ == "__main__":
    main()

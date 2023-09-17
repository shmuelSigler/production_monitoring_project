import requests
import time
import json
import random
import os


url = "https://chargeflow.io"
pagerduty_api_token = "e+9dgFyQBf-kzPmaSB3A"
pagerduty_api_url = "https://api.pagerduty.com/incidents"
headers = {
        "Authorization": f"Token token={pagerduty_api_token}",
        "Accept": "application/vnd.pagerduty+json;version=2",
        "Content-Type": "application/json",
        "From": "daniela@eatbright.co"
    }


def open_incident():

    data = {
        "incident": {
            "type": "incident",
            "title": "chargeflow.io website is down",
            "service": {
                "id": "P5A827W",    # From querystring in URL https://eatbright.eu.pagerduty.com/service-directory/P5A827W
                "type": "service_reference"
            }
        }
    }

    response = requests.post(
        pagerduty_api_url,
        headers=headers,
        data=json.dumps(data),
    )

    if response.status_code == 201:
        print("Incident opened successfully.")
        incident_id = response.json()["incident"]["id"]
        return incident_id
    else:
        print("Failed to open incident.")
        print(response.text)  # Print the error message, if any
        return None


def close_incident(incident_id):

    data = {
        "incident": {
            "type": "incident_reference",
            "status": "resolved"
        }
    }

    response = requests.put(
        f"{pagerduty_api_url}/{incident_id}",
        headers=headers,
        data=json.dumps(data),
    )

    if response.status_code == 200:
        print("Incident closed successfully.")
    else:
        print("Failed to close incident.")
        print(response.text)  # Print the error message, if any


def monitor_website():
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return True
    except requests.exceptions.RequestException:
        return False


def read_downtime():
    with open("downtime.json", "r") as json_file:
        data = json.load(json_file)
        return data.get("downtime"), data.get("incident_id")


def write_downtime(downtime, incident_id):
    data = {
        "downtime": downtime,
        "incident_id": incident_id,
    }
    with open("downtime.json", "w") as json_file:
        json.dump(data, json_file)


def main():
    current_hour = time.localtime().tm_hour
    current_min = time.localtime().tm_min
    downtime = 0
    previous_downtime, previous_incident_id = read_downtime()

    print("hour and minute:", current_hour, current_min)
    print("previous_downtime:", previous_downtime, "previous_incident_id:", previous_incident_id)

    if previous_downtime < 10:
        # Simulate failures at specific times (2:00am, 4:00am, 6:00am)
        if current_min == 0:
            downtime = random.randint(5, 15)
            is_up = False
        else:
            is_up = monitor_website()
            if previous_incident_id and is_up:
                close_incident(previous_incident_id)
        incident_id = None if is_up else open_incident()
    else:
        incident_id = previous_incident_id

    # Save the current downtime value and incident ID for the next run
    write_downtime(downtime, incident_id)

    print("new downtime:", downtime)


if __name__ == "__main__":
    main()

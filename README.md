# Production Monitoring Project 
This repository contains the code and configuration for a small-scale production monitoring project.

PagerDuty is an Incident Management System (IMS) that helps organizations manage incidents and coordinate response efforts. It provides on-call scheduling, alerting, and incident tracking features. By integrating InStatus with PagerDuty, i establish a connection between status monitoring and incident management processes.

 In the context of incident management, an "incident" represents an unexpected or unplanned event that disrupts normal operations and requires attention, investigation, and resolution. Incidents can range from system outages and service disruptions to security breaches and other issues that impact the functioning of a service or system.

##  Key Features                                                                   

- Periodically pinging chargeflow.io and simulating different response scenarios - using GitHub Actions to run the script at 10-minute intervals. 

- Simulate different responses, including failures for 5-15 minutes at the start of even hours (e.g., 2:00 AM, 4:00 AM, 6:00 AM).

- Webhook for real-time communication and incident management between these two systems: In Case of failure - open an incident at PagerDuty, which update the status page. As the incident progresses and is eventually resolved, PagerDuty can update the incident status and keep a detailed log of actions. 

 ## Run Locally

Before you begin, ensure you have the following prerequisites installed:

- Python 3 


Clone the project

```bash
  git clone https://github.com/shmuelSigler/production_monitoring_project-
```

Go to the project directory

```bash
  cd production_monitoring_project-
```


Run the application

```bash
  python3 main.py
```



## Documentation

[Publicly available Data ](https://chargeflow_sre.instatus.com/summary.json): The easiest way to get the current status of instatus's status page.

[Webhook](https://instatus.com/help/integrations/pagerduty): Use PagerDuty to automate the status page.

[Create an Incident in PagerDuty](https://developer.pagerduty.com/api-reference/a7d81b0e9200f-create-an-incident): Create an incident synchronously.



# Response Reporting Dashboard
  
## Goal: 
Build a dashboard for [VOST Europe](https://vosteurope.org/) to monitor Disinformation Reports and Response Times in Social Media Platforms, using Plotly and Dash. 
- Use this repo to work on the dashboard together or create your own repo to build your own dashboard.
- See [Readme](https://github.com/Coding-with-Adam/response-reporting-dashboard/blob/main/README.md) for the dashboard guideline.

## Problem:
When citizens flag content on very large online platforms (VLOPS) as disinformation or scam/frauds , the social media platforms respond that they will investigate and take action if needed. However, it is very challenging to follow up on the actions taken by these platforms. The main challenge is the lack of a tracking system to: 1) measure the number of reports made; 2) measure the follow-up actions taken in response and 3) measure the time it takes for VLOPS to answer those reports.

## Solution: 
[VOST Europe](https://vosteurope.org/), as a signatory of the Code of Practice on Disinformation, would like us to build a tracking app to monitor the response, and response times of VLOPS, to flags made by non-VLOPS’ signatories of the Code of Practice on Disinformation. The app will be used by VOST volunteers to create the reports and track all the subsequent actions taken by the VLOPS.

## Timeline:
April 1 to April 30. 

## Community Support:
Our [Project Monday meet-ups](https://charming-data.circle.so/c/events/project-mondays-84f00d) will be used to discuss this project and share feedback with each other. Also, please make sure to join the [Project Chats space](https://charming-data.circle.so/c/charming-data-chats/), because that is where we will communicate offline about the project and support each other along the way.  


# Structure of Response Reporting Dashboard
You can either use this repo to work on the dashboard together or create your own repo and design your own dashboard.

However, at minimum, to be considered by VOST Europe the dashboard should include the following elements:

- An internal-facing page ([see example](https://github.com/Coding-with-Adam/response-reporting-dashboard/blob/main/iternal.py)) that vetted volunteers will use to note social media reports:
    - Vetted user (predefined list)
    - Social media platform being reported (predefined list)
    - Link of content being reported
    - Report type (predefined list)
    - Time of report made
    - Response type (predefined list)
    - Response notes
    - Time of response

- a data-insights page that offers data visualizations on all the reports. At minimum it should include visualizations on:
    - Total reports grouped by social media platform
    - Type of report grouped by platform
    - Average response time grouped by platform
    - Reports’ response grouped by platform

- an application page allowing people to apply to become vetted users of the dashboard
- a homepage 

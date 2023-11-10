# Realtime-public-transport-STIB-MIVB
Courses project (Data exchange and database courses) in industrial IT engineer (HE2B - ISIB) in first master.

## Instructions
The aim of the project is to exchange data between two databases.
To carry out the transfer, we need to use the Python language.
The transfer must be made via an XML file and must be checked by an XSD to ensure that the structure is respected (and stop the process if necessary).
In order for this to be visible between the two databases, we were asked to create an XHTML file (correctly formatted HTML) using an XSLT file to enable the XML to be converted into XHTML.

In order :
* Database 1
* Python : get data
* Python : transform into a specific XML file (keep only some data or merge some tables and change structure)
* Python : compare the XML with an XSD file (and valid the structure)
* Python : create a XHTML file using a XSLT file (for formating)
* Python : push data in the second database (one or more table)
* Database 2

## Adaptations and choices
My choice of project was a site (XHTML) that displays the remaining waiting time for Brussels transport at the nearest stops.
In my case STOCKEL, which groups together several transport lines (and therefore stops).
The teacher authorised me to use an API as my first database.

The display therefore had to be dynamic.
On the STIB/MIVB (Société de Transport Intercomunaux Bruxellois) API, we are entitled to 10,000 requests per day, i.e. about one every 10 seconds.
As the API returns a time of passage and not the time remaining, I have estimated that calling the API every 30 seconds is sufficient. However, I refresh the web page every 10 seconds (to recalculate the remaining time between the API time and the current time, which can change at any time).

## Features
1. Real-Time Information: The project displays real-time information for public transportation services. It shows details such as departure times, line numbers, directions, and service status (alerts/messages). 
2. Display: The information is presented in a table format, making it easy for users to access and understand.
3. [NEXT COMMIT I HOPE] Sorting by Lefttime: The code includes a feature to sort the table based on the "lefttime" values, ensuring that the next departures are listed in ascending order of time.
4. Countdown Timer: The code calculates the time difference between the current time and the scheduled departure time, displaying the time left for the next departure.
5. Alert and Message Handling: The project handles alert and message information, distinguishing between regular departures and special messages like "Ligne déviée" (deviated line), "Fin de service" (end of service) and "Dernier passage" (last departure). Alerts and messages are displayed appropriately.
6. Removing Passed Times: The code identifies and removes rows with departure times that have already passed. If a row contains an alert or message, only the time is removed, while other rows without alerts and passed times are completely removed.
7. Dynamic Updates: The code is set to automatically update the information every 10 seconds (for the web page) and every 30 seconds (for request to API), ensuring that users have access to the latest information.
8. Styling: The code includes CSS styling to enhance the visual presentation of the information, including icons for indicating the current status.
9. Responsive Design: The project have a responsive design to adapt to different screen sizes and devices.
10. XML Namespace: The HTML document includes XML namespaces (e.g., xmlns and xmlns:xs), which may be used for validation or other purposes.

## Tags
<span>Developed with : <a href="https://code.visualstudio.com/" target="_blank"><image src="https://img.shields.io/badge/Visual Studio Code-v1.84.1-007ACC.svg?logo=visual-studio-code&logoColor=007ACC&style=flat"></a></span>


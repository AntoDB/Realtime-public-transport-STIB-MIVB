import requests
import xml.etree.ElementTree as ET
import ast # string representation of list to list using ast.literal_eval()
from colorama import Fore # For Colors in terminal
from lxml import etree  # Import lxml for check with XSD and XSLT transformations (parse XML)
import time # To redo the code every X second(s)
import mysql.connector # For the Maria database
from datetime import datetime # Parse to datetime for DB

import json

# Load the configuration from the JSON file
with open('./config.json') as config_file:
    config = json.load(config_file)

# Access the values
api_key = config['API_KEY']
db_user = config['DB_USER']
db_password = config['DB_PASSWORD']


# Define the API URL and query parameters
url = 'https://stibmivb.opendatasoft.com/api/records/1.0/search/'
params = {
    'dataset': 'waiting-time-rt-production',
    #'q': '8161',
    'lang': 'fr',
    'rows': '-1'
}

# Define the headers with your API key
headers = {
    'Authorization': api_key,
}

# Define the list of allowed "pointid" values (pointid is the dock of a transport line for an unique direction)
allowed_pointids = [8161, 8162, 1252, 1302, 6474, 6475]

# Function to convert a string containing a list to an actual list
def convert_string_to_list(string_value):
    try:
        return ast.literal_eval(string_value) # Converting string to list
    except (ValueError, SyntaxError):
        return string_value  # Return the original string if conversion fails
    
# Convert JSON data to XML (recussive function)
def json_to_xml(json_data, parent=None):
    """
    Input:
        json_data: This is the JSON data that needs to be converted to XML.
        parent: This is the XML element under which the converted data will be added as child elements.
    """
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key != "datasetid" and key != "recordid" and key != "record_timestamp": # Remove/Filter unless part from JSON for XML

                if key == "fields": # If one of the field for a station is one of you want
                    if value["pointid"] in allowed_pointids : # If the reference number of the station is on the selected list
                        element = ET.Element(key)
                        parent.append(element)
                        json_to_xml(value, element)

                else:
                    element = ET.Element(key)
                    parent.append(element)

                    if key == "passingtimes":
                        passingtimes = convert_string_to_list(value) # Because the value of "passingtimes" is a string of a list and not a list
                        if len(passingtimes) < 5:
                            for item in passingtimes:
                                vehicle = ET.Element("vehicle")
                                element.append(vehicle)
                                json_to_xml(item, vehicle)
                        else:
                            json_to_xml(passingtimes, element)
                    else:
                        json_to_xml(value, element)
                        

    elif isinstance(json_data, list):
        for item in json_data:
            json_to_xml(item, parent)
    else:
        parent.text = str(json_data)


# Verification of XML with the XSD file and print if it's good or not
def xml_valid():
    # Define the XML file and XSD schema file paths
    xml_file = "./output.xml"
    xsd_schema = "./schema-definition.xsd"

    # Load the XML file
    xml_tree = etree.parse(xml_file)

    # Load the XSD schema
    xsd_tree = etree.parse(xsd_schema)
    xsd_schema = etree.XMLSchema(xsd_tree)

    # Validate the XML against the XSD schema
    is_valid = xsd_schema.validate(xml_tree)

    if is_valid:
        print(Fore.GREEN + "XML is valid according to the XSD schema." + Fore.RESET)
        return True
    else:
        print(Fore.RED + "XML is not valid according to the XSD schema." + Fore.RESET)
        print(xsd_schema.error_log)
        return False

# Function to add a number in attribute to every vehicle in the XML
def add_attribute_vehicle_from_xml(tree):
    # Load your XML and XSLT files
    try:
        attribute_number = 0
        for vehicle in tree.findall(".//vehicle"):
            vehicle.set("vehicle_number", str(attribute_number))
            attribute_number += 1
    except Exception as e:
        print(Fore.RED + f"Error during XSLT changement by adding attribute: {e}" + Fore.RESET)


# Function to convert XML to XHTML using XSLT
def transform_xml_to_xhtml(xml_file, xslt_file, output_file):
    try:
        xml_doc = etree.parse(xml_file)
        xslt_doc = etree.parse(xslt_file)
        transform = etree.XSLT(xslt_doc)
        result = transform(xml_doc)
        with open(output_file, 'wb') as f:
            f.write(etree.tostring(result, pretty_print=True, method="html"))
        print(Fore.GREEN + "Transformed XML to XHTML successfully." + Fore.RESET)
    except Exception as e:
        print(Fore.RED + f"Error during XSLT transformation: {e}" + Fore.RESET)

def main():
    global root
    # Make a GET request to the API
    response = requests.get(url, params=params, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        print(data)

        # Create an XML element
        root = ET.Element("data")

        json_to_xml(data, root)
        print(Fore.GREEN + "Changed the JSON to XML." + Fore.RESET)

        # Create an ElementTree object
        tree = ET.ElementTree(root)       

        # Add a number in attribute to every vehicle in the XML
        add_attribute_vehicle_from_xml(tree)
        print(Fore.GREEN + "Changed the XML file. Add number in attribute for every vehicle." + Fore.RESET)
        
        # Write to an XML file
        tree.write("output.xml")
        print(Fore.GREEN + "Wrote a xml output file." + Fore.RESET)

        if xml_valid():
            transform_xml_to_xhtml("output.xml", "transform.xslt", "output.xhtml")

            print(Fore.GREEN + "Transformed XML to XHTML and saved as output.xhtml." + Fore.RESET)
        else:
            print(Fore.RED + "Stop code here (not put data into a DB and not create website)." + Fore.RESET)
    else:
        print(f"{Fore.RED} Request failed with status code: {Fore.RESET}\n{response.status_code}")

# ===================== #
#        DataBase
# ===================== #

# Function to create the database and tables
def create_database_and_tables():
    global connection
    # Connect to MariaDB (you can use different parameters if necessary)
    connection = mysql.connector.connect(
        host="localhost",  # Use the Docker container's hostname or IP
        user= db_user,  # Use the appropriate MariaDB username
        password= db_password  # Replace with your database password
    )
    
    # Create a cursor object to execute SQL statements
    cursor = connection.cursor()

    # Create a new database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS stib_data")

    # Switch to the new database
    cursor.execute("USE stib_data")

    # Create the point_data table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS point_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            pointid INT NOT NULL,
            lineId INT NOT NULL,
            destination VARCHAR(255) NOT NULL
        )
    """)

    # Create the vehicle_data table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicle_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            lineId INT NOT NULL,
            destination VARCHAR(255) NOT NULL,
            expectedArrivalTime DATETIME NOT NULL,
            message VARCHAR(255)
        )
    """)

    # Commit changes and close the connection
    connection.commit()
    #connection.close()

# Function to insert data into the point_data table if it doesn't already exist
def insert_point_data(cursor, pointid, lineId, destination):
    # Check if a row with the same pointid, lineId, and destination exists
    cursor.execute("SELECT 1 FROM point_data WHERE pointid = %s AND lineId = %s AND destination = %s LIMIT 1", (pointid, lineId, destination))
    
    if not cursor.fetchone():
        # If no matching row exists, insert the data
        cursor.execute("INSERT INTO point_data (pointid, lineId, destination) VALUES (%s, %s, %s)", (pointid, lineId, destination))

# Function to insert data into the vehicle_data table
def insert_vehicle_data(cursor, lineId, destination, expectedArrivalTime, message):
    # Convert the expectedArrivalTime string to a datetime object
    expectedArrivalTime = datetime.strptime(expectedArrivalTime, "%Y-%m-%dT%H:%M:%S%z")

    cursor.execute("INSERT INTO vehicle_data (lineId, destination, expectedArrivalTime, message) VALUES (%s, %s, %s, %s)", (lineId, destination, expectedArrivalTime, message))

def update_database():
    # Create a cursor object to execute SQL statements
    cursor = connection.cursor()

    # Iterate over the XML data and insert into the database
    for field in root.findall(".//fields"):
        pointid = field.find(".//pointid").text

        for vehicle in field.findall(".//vehicle"):
            lineId = vehicle.find(".//lineId").text

            destination_elm = vehicle.find(".//destination/fr")
            destination = destination_elm.text if destination_elm is not None else ""

            expectedArrivalTime = vehicle.find(".//expectedArrivalTime").text

            message_element = vehicle.find(".//message/fr")
            message = message_element.text if message_element is not None else ""

            # Insert data into tables
            insert_point_data(cursor, pointid, lineId, destination)
            insert_vehicle_data(cursor, lineId, destination, expectedArrivalTime, message)
    
    connection.commit()


if __name__ == "__main__":
    # Call the function to create the database and tables
    create_database_and_tables()

    iteration = 0
    while True:
        iteration += 1
        main()
        update_database()
        print(f"Number of times the code has been executed: {iteration}")

        time.sleep(30) # Sleep for 30 seconds

    # Close the connection
    connection.close()




# ===== NEXT UPDATES ===== #

# Add attribute for single data. eg.: lineid
# Get if the database was good set, data pushed, etc
# In the JS: Sorted by current time

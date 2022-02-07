# 28/06/2021. Check Aspire lists for 404 or 410 http status
# This script is greatly improved to get the list and items data from Aspire's Redshift database
# The previous version, that used a *csv input, is still valid for people that do not have
# Aspire Advanced MIS

# 08/07/2021
# Using the JDBC connection. (I found out  that my previous driver would cost £8k in licencing!

# 03/02/2022
# use head requests rather than get

# Tim Graves. t.c.graves@sussex.ac.uk. University of Sussex Library

import jaydebeapi as jay
import os
from csv import writer
import requests
import re
import yaml

# read configuration from file
with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
	
# Connect to Aspire Advanced MIS, and retrieve all currently published lists

host=cfg['database']['host']
database=cfg['database']['database']
username=cfg['database']['username']
password=cfg['database']['password']
port = "5439"

# Redshift JDBC class name
jdbc_driver_name = "com.amazon.redshift.jdbc.Driver"

# Redshift JDBC driver path
# You will need to change this to reflect where you have saved the driver
jdbc_driver_loc = os.path.join(r'/home/alfi1/redshift-jdbc42-2.0.0.4.jar')

# JDBC connection string
connection_string='jdbc:redshift://'+ host+':'+port+'/'+database

url = '{0}:user={1}; password={2}'.format(connection_string, username, password)

#print("Connection String: " + connection_string)

# Establish JDBC connection
conn = jay.connect(jdbc_driver_name, connection_string, {'user': username, 'password': password},
jars=jdbc_driver_loc)

curs = conn.cursor()
curs.execute(cfg['sql'])
results = curs.fetchall()

# set request headers
headers = { 'User-Agent', 'Aspire-Link-Checker'}

############
		
# Function to write out the results
def writeOut(output_data):
    with open('all_items_link_report.csv', 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(output_data)
        f_object.close	

# Add a header line
with open('all_items_link_report.csv', 'w') as f_object:
   writer_object = writer(f_object)
   writer_object.writerow(['Status', 'Course', 'URL', 'Item link'])
   f_object.close	

# Loop through the results, checking the URL status
for each_one in results:

    item_link = each_one[0]
    course = each_one[1]
    the_url = each_one[2]
	
 ## Handle any multiple URLs in the URL field

    if '; http' in the_url:

        line = the_url.strip()
	
        split_up = line.split("; http")
    		
        for idx, each_url in enumerate(split_up):

            temp_url = each_url.replace('http' , '')
            final_url = 'http' + temp_url
            #print(final_url)
            try:
                response = requests.head(final_url, headers=headers, timeout=15)   # Original timeout 15
                status = response.status_code
            except:
                status  = 408
				
            # Write to file
            output_data = [status, course, final_url, item_link]
            if status == 404 or status == 410:
                writeOut(output_data)

## End of processing the duplicate URLs

    else: # Carry on and process the entries without duplicate URLs
		
        try:
            response = requests.head(the_url, headers=headers, timeout=15)   # Original timeout 15
            status = response.status_code
        except:
            status  = 408
        
        if status == 404 or status == 410:
        #if status >1:   # testing purposes
	
            print(status)
            # Write to file
            output_data = [status, course, the_url, item_link]
            writeOut(output_data)
			

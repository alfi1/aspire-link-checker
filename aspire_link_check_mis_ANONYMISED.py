# 28/06/2021. Check Aspire lists for 404 or 410 http status
# This script is greatly improved to get the list and items data from Aspire's Redshift database
# The previous version, that used a *csv input, is still valid for people that do not have
# Aspire Advanced MIS

# This will only work on a machine that has been authorised by Talis
# to access the Advanced MIS


# This uses psycopg2 to make the connection.
# Works on Python running in either Linux or Windows

# Tim Graves. University of Sussex Library. t.c.graves@sussex.ac.uk
  
import psycopg2
from csv import writer
import requests
import re

# Connect to Aspire Advanced MIS, and retrieve all currently published lists
# You will need to add your own database details
con=psycopg2.connect(dbname= 'YOUR-DATABASE', host='YOUR-HOST-FOR-ADVANCED-MIS', port= '5439', user= 'USERNAME', password= 'PASSWORD')

# You shouldn't need to change anything below here
# Apart from the time_period as each year passes

cur = con.cursor()

# The SQL statement
cur.execute("select i.item_url, l.title, i.web_address from f_rl_items i, f_rl_lists l where i.list_guid = l.list_guid and i.status = 'Published' and i.web_address != '' and i.time_period = '21/22'")

results = cur.fetchall()

cur.close() 

		
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
	
 ## Handle any multiple URLs in the URL field (I don't know if this is only a Sussex problem!)

    if '; http' in the_url:

        line = the_url.strip()
	
        split_up = line.split("; http")
    		
        for idx, each_url in enumerate(split_up):

            temp_url = each_url.replace('http' , '')
            final_url = 'http' + temp_url

            try:
                response = requests.get(final_url, timeout=15) 
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
            response = requests.get(the_url, timeout=15)   # Original timeout 15
            status = response.status_code
        except:
            status  = 408
        
        if status == 404 or status == 410:
	
            print(status)
            # Write to file
            output_data = [status, course, the_url, item_link]
            writeOut(output_data)
			
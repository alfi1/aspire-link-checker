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
import yaml

# read configuration
with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

# Connect to Aspire Advanced MIS, and retrieve all currently published lists
con = psycopg2.connect(
    dbname=cfg['database']['database'],
    host=cfg['database']['host'],
    port='5439',
    user=cfg['database']['username'],
    password=cfg['database']['password']
)

cur = con.cursor()

# The SQL statement
cur.execute(cfg['sql'])

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
			
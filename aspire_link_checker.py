# Go through the Aspire all_items *csv file in two passes
# Pass 1 extracts the three columns we need
# Pass2 extracts only those records with a valid 'web address' in column 3
# This one successfully picks up multiple URLs in one line
# Tim Graves. University of Sussex Library. March 2021

import pandas as pd
import requests
import re
from csv import writer 

original_filename = 'all_list_items_2021_03_11.csv'

# In a normal run, you shouldn't need to edit anything below this point

#Read in  the original file
pass1 = pd.read_csv(original_filename) 

# Extract the three columns we need
my_output = pass1[['Item Link', 'List Appearance', 'Web Address']]

# Write them to file
my_output.to_csv('all_items_output.csv', index=False)

## Second pass, to select only records that have a 'web address'

# Read in the file you produced as the output of pass 1
pass2 = pd.read_csv("all_items_output.csv") 

# Create a boolean series False for NaN values (i.e. where 'web address' does NOT test positive for being NaN (not a number)
# Ludicrous syntax, but it took ages to come up with, and works
bool_series = pd.notnull(pass2.iloc[:, 2])
 
# write out to a second file
pass2[bool_series].to_csv('all_items_output2.csv', index=False)

# This gives us the file we want to send into the link checker

#### FOR TESTING ONLY, select a subset of the output from the second pass
#test_pass = pd.read_csv("all_items_output2.csv")
#test_batch = test_pass.head(500)
#test_batch.to_csv('all_items_output_sample.csv', index=False)
############################################

# Start the link checking here

# Turn the write out into a function
def writeOut(output_data):
    with open('all_items_link_report.csv', 'a') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(output_data)
        f_object.close	

#fh = open("all_items_output_sample.csv")
fh = open("all_items_output2.csv")

# r , for reading.
# w , for writing.
# a , for appending.

with open('all_items_link_report.csv', 'w') as f_object:
   writer_object = writer(f_object)
   writer_object.writerow(['Status', 'Course', 'URL', 'Item link'])
   f_object.close	

for line in fh:

    #print(line)
        
    split_up = line.split(",")
    item_link = split_up[0].rstrip()
    course = split_up[1]
    
    try:
        the_url = split_up[2].rstrip()
        
    except:
        the_url = 'Unrecognised URL'
    
 ## Need to intercept the multiple URLs at this point

    if '; http' in the_url:

        line = the_url.strip()
	
        split_up = line.split("; http")
    		
        for idx, each_url in enumerate(split_up):

            temp_url = each_url.replace('http' , '')
            final_url = 'http' + temp_url
            #print(final_url)
            try:
                response = requests.get(final_url, timeout=15)   # Original timeout 15
                status = response.status_code
            except:
                status  = 408
				
            # Write to file
            output_data = [status, course, final_url, item_link]
            if status == 404:
                writeOut(output_data)

			
## End of processing the duplicate URLs

    else: # Carry on and process the entries without duplicate URLs
		
        try:
            response = requests.get(the_url, timeout=15)   # Original timeout 15
            status = response.status_code
        except:
            status  = 408
        
        if status == 404:
	
            # Write to file
            output_data = [status, course, the_url, item_link]
            writeOut(output_data)
				
 	
fh.close()



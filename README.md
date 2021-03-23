# aspire-link-checker
To check through URLs in Aspire reading lists, and report on any dead links.

Written in Python 3. Will run on Windows, Linux or Unix.

First download an 'all_list_items' CSV report from Aspire.
Move aspire_link_checker.py to the directory from which you intend to run it.

The only line of the file that should need editing is the one that defines the source file downloaded from Aspire:
original_filename = 'all_list_items_2021_03_11.csv'

Run!

The script takes hours to run. By example, on 22/03/2021, I ran it against all our current reading lists. It took 12 hours to run, and detected 208 dead links.

When finished, it will output the report file 'all_items_link_report.csv', which contains:
The http Status (always 404, unless you tweak the code)
The reading list that contains the broken link
The broken link itself
The 'Item link', which is the link in Aspire from which the dead URL was called.

****

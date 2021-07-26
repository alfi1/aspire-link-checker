# aspire-link-checker
To check through all URLs in Aspire reading lists, and report back on any dead links.

Written in Python 3. Will run on Windows, Linux or Unix.
Because it takes so long to run, it is best to run in on a machine that you can leave alone for hours, or (better) as nohup on Linux. 

## The different files explained
There is a file for all users of Talis Aspire:

- `aspire_link_checker.py` - For sites that do NOT have Aspire Advanced MIS.
- `aspire_link_check_mis_windows.py` - For those with access to Advanced MIS, and who want to run Python in Windows.
- `aspire_link_check_mis_jdbc.py` - For users of Advanced MIS, who want to run on a Windows Linux subsystem or straight Linux machine.

My preference is `aspire_link_check_mis_jdbc.py`, as running the script on Linux opens up more options for scheduling via cron,
automatically emailing the results, or automatically SFTPing them to a specific location. It is the most versatile choice.

There is a wiki page that explains how to run each file, depending on which version you choose to use.

## Note on run time
The script takes hours to run. By example, on 22/03/2021, I ran it against all our current reading lists. It took 12 hours to run, and detected 208 dead links.

When finished, it will output the report file 'all_items_link_report.csv', which contains:
- The http Status (always 404, unless you tweak the code)
- The reading list that contains the broken link
- The broken link itself
- The 'Item link', which is the link in Aspire from which the dead URL was called.

Feel free to tune and tweak the code. If you make it better or faster, please let me know.

You could certainly make it significantly faster by reducing the time that the script checks each URL:
  response = requests.get(final_url, timeout=15)

t.c.graves@sussex.ac.uk 

****

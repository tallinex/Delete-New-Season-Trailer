# Delete-New-Season-Trailer
Finds new season trailers and deletes them

<h2>For Synology NAS:</h2>
Download the new_season_alert.py file and store in a convenient location e.g. /scripts/Delete_New_Season_Trailer/Delete_New_Season_Trailer.py<br>

<h2>Configure the script:</h2>
open the Delete_New_Season_Trailer.py file and set the variables at the top<br>
PLEX_URL = 'http://localhost:32400'  # Change to your Plex server URL<br>
PLEX_TOKEN = 'YOUR_PLEX_TOKEN_HERE'  # Replace with your Plex token<br>
LABEL_NAME = 'New Season'  # The label to search for on TV shows<br>
REPORT_MODE = True  #True will report only, change to False to actually delete episodes<br>


<h2>set up a scheduled task:</h2>
1: Control Panel --> Task Scheduler<br>
2: Create -->Scheduled Task --> User Defined Script<br>
3: General tab; Task Name - e.g. Delete New Season Trailer; User - root<br>
4: Schedule; Repeate - Daily; Start Time - eg 17 : 00 (for 5pm)<br>
5: Task Settings; user-defiend script - python3 /volume1/scripts/new_season_alerts/Delete_New_Season_Trailer.py<br>
6: Press ok to save<br>

The task will run every day at the set time and push an alert to your discord webhook

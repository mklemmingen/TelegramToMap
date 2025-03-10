# TelegramToMap

Created to quickly look up the location of threats as they come in to judge the need for different alarm reactions (corridors, subways etc.).

Scans incoming messages in Telegram groups for Ukrainian air alarms, extracting location data of UAVs, missiles, and planes. Adds a red marker to the map in QGIS, which turns white after some time and eventually disappears.



1. Install QGIS

2. Install the Plugin QuickMapServices (Plugins > Manage and Install Plugins > look for it and install)

3. Activate the plugins layer in Web > QuickMapServices > OSM > OSM Standard to add the OpenStreetMap layer

4. Download the ukraine shapefile from https://gadm.org/download_country.html and add it to Layers via Layer > Add Layer > Add Vector Layer and selecting the downloaded shapefile

5. only select as checked UKR_1.shpm and style it after a dopple click to have a opacity of 30 (or what you prefer)

6. open the python console in plugins > python and run the script in the location you have put it

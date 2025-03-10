# TelegramToMap

Created to quickly look up the location of threats as they come in to judge the need for different alarm reactions (corridors, subways etc.).

Scans incoming messages in Telegram groups for Ukrainian air alarms, extracting location data of UAVs, missiles, and planes. Adds a red marker to the map in QGIS, which turns white after some time and eventually disappears.

### -- QGIS

1. Install QGIS

2. Install the Plugin QuickMapServices (Plugins > Manage and Install Plugins > look for it and install)

3. Activate the plugins layer in Web > QuickMapServices > OSM > OSM Standard to add the OpenStreetMap layer

4. Download the ukraine shapefile from https://gadm.org/download_country.html and add it to Layers via Layer > Add Layer > Add Vector Layer and selecting the downloaded shapefile

5. only select as checked UKR_1.shpm and style it after a dopple click to have a opacity of 30 (or what you prefer)

### -- Telegram

6. Create a New Bot with BotFather
   
  Open Telegram and search for the user @BotFather.

  Start a chat with BotFather and use the command /newbot.

  Follow the prompts to:

   Name your bot.

   Choose a username for your bot (must end in bot, e.g., MySampleBot).

   Receive your bot token.

7. create a .env file in the root of your project where the qgis project file and the script is, and write a line with:

   TELEGRAM_BOT_TOKEN=your_bot_token_here

8. get the chatIDs by (one way of a couple) opening telegram in the browser, going to the group and copying the - and numbers after the #

### -- Installing packages into QGIS python 

Step-by-Step Guide to Install Python Packages in QGIS

For Windows:

Open the OSGeo4W Shell:

Go to the Start menu and search for "OSGeo4W Shell".

Open the OSGeo4W Shell.

Install the telegram and other required modules:

Use the following commands to install the necessary packages:

pip install python-telegram-bot geopy python-dotenv

For macOS/Linux:

Open a terminal.

Install the telegram and other required modules:

Use the following commands to install the necessary packages:

pip install python-telegram-bot geopy python-dotenv

### -- QGIS

9. open the python console in plugins > python and put each of the following lines in one by one:

import telegram

import geopy

import dotenv

import os

import sys

script_dir = os.path.dirname(QgsProject.instance().fileName())

sys.path.append(script_dir)

script_path = os.path.join(script_dir, 'telegramToQGIS.py')

exec(open(script_path).read())

----------------------
### Pseudocode
---------------------

1. Import necessary libraries and modules
   - os, time, asyncio, telegram, dotenv, geopy, qgis, PyQt5

2. Load environment variables from .env file

3. Retrieve the Telegram bot token from environment variables

4. Set up Telegram bot with the retrieved token
   - Define channel usernames to monitor

5. Set up Geopy geolocator

6. Set up QGIS layer for storing locations
   - Define attributes for the layer (name, timestamp)
   - Add the layer to the QGIS project

7. Define function to add a circle to the QGIS layer
   - Create a feature with latitude, longitude, and name
   - Set geometry and attributes for the feature
   - Add the feature to the layer

8. Define function to update circle colors based on timestamp
   - Calculate elapsed time since the feature was added
   - Delete features older than 30 minutes
   - Update color intensity based on elapsed time
   - Set renderer for the layer

9. Define asynchronous function to monitor Telegram channels
   - Get updates from Telegram bot
   - Check if the update is from monitored channels
   - Geocode the text from the update
   - If location is found and is in Ukraine, add a circle to the layer
   - Print appropriate messages based on location status
   - Update circle colors

10. Define function to start monitoring with QTimer
    - Create a new event loop
    - Run the monitor_channels function in the event loop

11. Set up QTimer to call start_monitoring every 60 seconds

12. Keep the script running with QApplication

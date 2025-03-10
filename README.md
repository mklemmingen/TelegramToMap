# TelegramToMap

Created to quickly look up the location of threats as they come in to judge the need for different alarm reactions (corridors, subways etc.).

Scans incoming messages in Telegram groups for Ukrainian air alarms, extracting location data of UAVs, missiles, and planes. Adds a red marker to the map in QGIS, which turns white after some time and eventually disappears.

-- QGIS

1. Install QGIS

2. Install the Plugin QuickMapServices (Plugins > Manage and Install Plugins > look for it and install)

3. Activate the plugins layer in Web > QuickMapServices > OSM > OSM Standard to add the OpenStreetMap layer

4. Download the ukraine shapefile from https://gadm.org/download_country.html and add it to Layers via Layer > Add Layer > Add Vector Layer and selecting the downloaded shapefile

5. only select as checked UKR_1.shpm and style it after a dopple click to have a opacity of 30 (or what you prefer)

-- Telegram

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

9. open the python console in plugins > python and put each of the following lines in one by one: 

import os

import sys

script_dir = os.path.dirname(QgsProject.instance().fileName())

sys.path.append(script_dir)

script_path = os.path.join(script_dir, 'telegramToQGIS.py')

exec(open(script_path).read())

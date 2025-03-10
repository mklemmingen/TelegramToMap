import os
import time
import asyncio
import telegram
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
from qgis.core import QgsProject, QgsPointXY, QgsGeometry, QgsFeature, QgsVectorLayer, QgsSymbol, QgsRendererCategory, QgsCategorizedSymbolRenderer
from PyQt5.QtCore import QVariant, QTimer
from PyQt5.QtGui import QColor

# Load environment variables from .env file
load_dotenv()

# Retrieve the Telegram bot token
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

# Telegram bot setup
bot = telegram.Bot(token=bot_token)
channel_usernames = ['@war_monitor', '@eRadarrua']

# Geopy setup
geolocator = Nominatim(user_agent="geoapiExercises")

# QGIS setup
layer = QgsVectorLayer("Point?crs=EPSG:4326", "Locations", "memory")
provider = layer.dataProvider()
provider.addAttributes([QgsField("name", QVariant.String), QgsField("timestamp", QVariant.Double)])
layer.updateFields()
QgsProject.instance().addMapLayer(layer)

# Function to add a circle
def add_circle(lat, lon, name):
    feature = QgsFeature()
    feature.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(lon, lat)))
    feature.setAttributes([name, time.time()])
    provider.addFeature(feature)
    layer.updateExtents()

# Function to update circle colors
def update_circle_colors():
    current_time = time.time()
    features = layer.getFeatures()
    for feature in features:
        timestamp = feature['timestamp']
        elapsed = current_time - timestamp
        if elapsed > 1800:  # 30 minutes
            layer.dataProvider().deleteFeatures([feature.id()])
        else:
            color_intensity = 255 - int((elapsed / 1800) * 255)
            symbol = QgsSymbol.defaultSymbol(layer.geometryType())
            symbol.setColor(QColor(255, color_intensity, color_intensity))
            renderer = QgsCategorizedSymbolRenderer("name", [QgsRendererCategory(name, symbol, name)])
            layer.setRenderer(renderer)

# Function to monitor Telegram channels
async def monitor_channels():
    updates = await bot.get_updates()
    for update in updates:
        if update.channel_post:
            channel_username = update.channel_post.chat.username
            if channel_username in channel_usernames:
                text = update.channel_post.text
                location = geolocator.geocode(text)
                if location:
                    if "Ukraine" in location.address:
                        print(f"Location found: {text} -> {location.address}")
                        add_circle(location.latitude, location.longitude, text)
                    else:
                        print(f"Location found but not in Ukraine: {text} -> {location.address}")
                else:
                    print(f"Location not found: {text}")
    update_circle_colors()

# Function to start monitoring with QTimer
def start_monitoring():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(monitor_channels())

# Set up QTimer to call start_monitoring every 60 seconds
timer = QTimer()
timer.timeout.connect(start_monitoring)
timer.start(60000)  # 60 seconds

# Keep the script running
from qgis.PyQt.QtWidgets import QApplication
app = QApplication.instance()
if app is None:
    app = QApplication([])
app.exec_()
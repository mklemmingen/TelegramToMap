import time
import telegram
from geopy.geocoders import Nominatim
from qgis.core import QgsProject, QgsPointXY, QgsGeometry, QgsFeature, QgsVectorLayer, QgsSymbol, QgsRendererCategory, QgsCategorizedSymbolRenderer
from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QColor

# Telegram bot setup
bot = telegram.Bot(token='YOUR_TELEGRAM_BOT_TOKEN')
chat_ids = ['CHAT_ID_1', 'CHAT_ID_2']

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

# Function to monitor Telegram chats
def monitor_chats():
    while True:
        for chat_id in chat_ids:
            updates = bot.get_updates(chat_id=chat_id)
            for update in updates:
                if update.message:
                    text = update.message.text
                    location = geolocator.geocode(text)
                    if location and "Ukraine" in location.address:
                        add_circle(location.latitude, location.longitude, text)
        update_circle_colors()
        time.sleep(60)

# Start monitoring
monitor_chats()
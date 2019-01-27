__version__ = "1.0.0"

import os
import logging

logger = logging.getLogger()

formatter = logging.Formatter(
  "[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s",
  "%Y-%m-%d %H:%M:%S %z"
)

if len(logger.handlers) > 0:
  logger.handlers[0].setFormatter(formatter)
else:
  consoleHandler = logging.StreamHandler()
  consoleHandler.setFormatter(formatter)
  logger.addHandler(consoleHandler)

LOG_LEVEL = os.environ.get("LOG_LEVEL") or "DEBUG"
logger.setLevel(logging.getLevelName(LOG_LEVEL))

try:
  from urllib.parse import urlparse
except ImportError:
  from urlparse import urlparse

from pymongo import MongoClient
import paho.mqtt.client as mqtt

DB = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/testroku")
MQ = os.environ.get("CLOUDMQTT_URL",
     os.environ.get("MQTT_URL", "mqtt://localhost:1883"))

mongo    = MongoClient(DB)
database = DB.split("/")[-1]
db       = mongo[database]

mq = mqtt.Client()

def connect():
  config = urlparse(MQ)
  if config.username and config.password:
    mq.username_pw_set(config.username, config.password)
  mq.connect(config.hostname, config.port)
  mq.loop_start()

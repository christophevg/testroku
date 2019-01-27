import logging
import time
import json

from . import db, mq, connect

stop = False

def on_connect(client, id, flags, rc):
  logging.debug("backend connected to MQ with result code {0} as {1}".format(
    str(rc), id
  ))
  if rc == 0:
    client.message_callback_add("inbox", on_cmd)
    client.subscribe("inbox")
    logging.debug("subscribed to inbox")

def on_cmd(client, id, msg):
  global stop
  msg = json.loads(str(msg.payload.decode("utf-8")))
  cmd = msg["cmd"]
  payload = msg["payload"]
  output = { "result" : "I received and processed: {0}".format(payload) }
  db.outbox.replace_one({"_id": cmd}, output, upsert=True)
  logging.debug("processed {0}".format(cmd))
  if cmd == "stop":
    stop = True

mq.on_connect = on_connect

connect()

while not stop:
  time.sleep(1)

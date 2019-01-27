import os
import logging
import json

logger = logging.getLogger()

from flask import Flask, request, render_template
import flask_restful
from flask_restful import Resource

from . import db, mq, connect

server = Flask(__name__)

@server.route("/")
def render_home():
  return render_template("index.html")

api = flask_restful.Api(server)

class Control(Resource):
  def get(self, cmd):
    return db.outbox.find_one({"_id": cmd}) or "sorry, no output..."
    
  def post(self, cmd):
    payload = request.get_json()
    mq.publish("inbox", json.dumps({ "cmd" : cmd, "payload": payload}) )

  def delete(self, cmd):
    db.outbox.remove({"_id" : cmd})

api.add_resource(Control,
  "/api/<string:cmd>"
)

connect()

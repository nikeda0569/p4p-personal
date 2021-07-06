import paho.mqtt.client as mqtt     # MQTTのライブラリをインポート
from database import db_session
from database import init_db
from models import Data

import datetime

# ブローカーに接続できたときの処理
def on_connect(client, userdata, flag, rc):
  print("Connected with result code " + str(rc))  # 接続できた旨表示
  client.subscribe("case10")  # subするトピックを設定 

# ブローカーが切断したときの処理
def on_disconnect(client, userdata, flag, rc):
  if  rc != 0:
    print("Unexpected disconnection.")

# メッセージが届いたときの処理
def on_message(client, userdata, msg):
  # msg.topicにトピック名が，msg.payloadに届いたデータ本体が入っている
  print("Received message '" + str(msg.payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))
  dt_now = datetime.datetime.today()
  if str(msg.payload) == "b'detection'":
    row = Data(date=dt_now,detection=1)
    db_session.add(row)
    db_session.commit()
  else:
    row = Data(date=dt_now,detection=0)
    db_session.add(row)
    db_session.commit()

# MQTTの接続設定
client = mqtt.Client()                 # クラスのインスタンス(実体)の作成
client.on_connect = on_connect         # 接続時のコールバック関数を登録
client.on_disconnect = on_disconnect   # 切断時のコールバックを登録
client.on_message = on_message         # メッセージ到着時のコールバック

client.connect("192.168.10.106", 1883, 60)  # 接続先は自分自身

client.loop_forever()                  # 永久ループして待ち続ける
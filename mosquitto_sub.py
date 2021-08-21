import paho.mqtt.client as mqtt     # MQTTのライブラリをインポート
from database import db_session
from database import init_db
from models import Data_D
from models import Data_L

import datetime

# ブローカーに接続できたときの処理
def on_connect(client, userdata, flag, rc):
  print("Connected with result code " + str(rc))  # 接続できた旨表示
  client.subscribe("kameneko0569")  # subするトピックを設定 

# ブローカーが切断したときの処理
def on_disconnect(client, userdata, flag, rc):
  if  rc != 0:
    print("Unexpected disconnection.")

# メッセージが届いたときの処理
def on_message(client, userdata, msg):
  # msg.topicにトピック名が，msg.payloadに届いたデータ本体が入っている
  print("Received message '" + str(msg.payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))

  x = str(msg.payload).split("'")
  print(len(x))
  print(x[0])

  if x[0] == 'b"detection=':
    dt_now = datetime.datetime.today()
    db_count = int(x[1])
    row = Data_D(date_detection=dt_now,detection=db_count)
    db_session.add(row)
    db_session.commit()
  
  elif x[0] == 'b"luminance value=':
    dt_now = datetime.datetime.today()
    db_count = int(x[1])
    row = Data_L(date_luminance=dt_now,luminance=db_count)
    db_session.add(row)
    db_session.commit()
  
  else:
    pass


# MQTTの接続設定
client = mqtt.Client()                 # クラスのインスタンス(実体)の作成
client.on_connect = on_connect         # 接続時のコールバック関数を登録
client.on_disconnect = on_disconnect   # 切断時のコールバックを登録
client.on_message = on_message         # メッセージ到着時のコールバック

client.connect("test.mosquitto.org", 1883, 60)  # 接続先は自分自身

client.loop_forever()                  # 永久ループして待ち続ける
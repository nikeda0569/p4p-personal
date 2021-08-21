#### p4p-personal

##### Heroku Web Dyno用ファイル
Posgresqlよりデーターを読み込みDashのWebフレームワークを使ってセンサーデーターをグラフ表示する。

- test_view.py (Dash用Pythonファイル)
- database.py (sqlalchemy用Database操作のファイル)
- models.py (sqlalchemy用Database model定義ファイル)
- Procfile (Heroku用Procfile)
- requirements.txt (Heroku用requirements.txt)

##### Heroku Worker Dyno用ファイル
mqttの通信を受けてPosgresqlにDatabaseに書き込みを行う。  
databaseはweb dyno上のposgresqlに書き込みを行う。

- mosquitto_sub.py (mqttのsubscriber及びdatabaseへの書き込み)
- database.py (web dynoと共通)
- models.py (web dynoと共通)
- Procfile (web dynoと共通)
- requirements.txt (web dynoと共通)

##### rasberrypi用ファイル
センサー用のPythonファイル。

- ADC0832.py (ADコンバーター用Pythonファイル)　
- photoresistor.py (輝度センサー用Pythonファイル)
- rpi_mqtt_pub.py (人感センサー用Pthonファイル)
- led-button.py (緊急通知ボタン用Pythonファイル)

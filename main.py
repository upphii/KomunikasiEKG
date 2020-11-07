import paho.mqtt.client as mqtt
import pymysql.cursors
import time
from time import sleep

# Connect to the database
connection = pymysql.connect(host='0.tcp.ngrok.io', #localhost
                             port=14912,
                             user='root',
                             password='root',
                             db='arrhythmia-detector-interface', #belajar_database
                             charset='utf8',   #'utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
print(connection)
userid=""
token = input ("Masukan token: ")
with connection.cursor() as cursor:
    tokenquery = 'SELECT * from `devices` where `token`="' + token + '"'
    cursor.execute(tokenquery)
    result = cursor.fetchone()
    userid=str(result["user_id"])
    print("user_id aktif " + str(result["user_id"]))



def kirimData(user_id="1",ecg_data="0"):
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `raws` (`id`, `user_id`, `data`, `created_at`, `updated_at`) VALUES (NULL, " + user_id + ", " + ecg_data + ", current_timestamp(), current_timestamp())"
            # sql = "INSERT INTO `ekg_datas` (`id`, `user_id`, `data`, `created_at`, `updated_at`) VALUES (NULL, " + user_id + ", " + ecg_data + ", current_timestamp(), current_timestamp())"
            if (ecg_data !="5000.00"): cursor.execute(sql)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        if (ecg_data !="5000.00"):
            connection.commit()
            print("data saved")
    except:
        print("error gan")

    # finally:
    #     connection.close()



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("LuthfiPubData")

count = False
nomor = 0

def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload,encoding='utf8',errors='strict')) #.encode('utf-8')
    # kirimData(ecg_data=str(msg.payload,encoding='utf8',errors='strict'))
    global nomor
    global count
    localtime = time.asctime(time.localtime(time.time()))
    print( str(nomor) + ". " + msg.topic + " " + msg.payload.decode() + " received at " + localtime)


    if (msg.payload.decode()=="5000.00"):
        count=True

    if ( count ):
        kirimData(user_id=userid, ecg_data=msg.payload.decode())
        nomor = nomor + 1



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.mqtt-dashboard.com", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

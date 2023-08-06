import os
import sys
import threading
import time
from multiprocessing import Process, Value, Array

PATH = os.path.abspath(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
sys.path.append(PATH)
print(PATH)

from src.winhye_common.mqtt.mqtt_base import MqttClint, MqttSendMessageException


def mqtt_test(index):
    mqtt_config = {
        "broker": "mqtt-cn-i7m2ceaxt07.mqtt.aliyuncs.com",
        "port": 1883,
        "topic": "reported_kaifa/AGV-S/#",
        "AccessKey_ID": "LTAI5tFbpMr1R4CVCbUePMWy",
        "AccessKey_Secret": "MJ2WWUbIKDg4UY5EbEsgQ983Lkfwff",
        "instance_id": "mqtt-cn-i7m2ceaxt07",
        "group_id": "GID_kaifa"
    }
    data = {
        "type": 1,
        "code": 200,
        "payload": {
            "id": "E41203294",
            "armed": "arm"
        }
    }
    handler = MqttClint(mqtt_config, thread=True)
    # t1 = threading.Thread(target=handler.client.loop_forever)
    # t1.setDaemon(True)
    # t1.start()
    # time.sleep(20)

    try:
        while True:
            handler.send_message("send_kaifa/AGV-S/aa", data)
            # print(index, handler.client_id, handler)
            time.sleep(2)
    except MqttSendMessageException:
        print(111111111111111111)


if __name__ == '__main__':
    # mqtt_test(1)
    p = Process(target=mqtt_test, args=(1,))
    p2 = Process(target=mqtt_test, args=(2,))
    print('Child process will start.')
    p.start()
    p2.start()
    p.join()
    p2.join()
    print("end")



from sense_hat import SenseHat
import requests
import datetime
import thread


def getserial():
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"

    return cpuserial


ider = {'API-IDENTIFIER': "" + getserial(), 'Content-Type': 'application/json'}

print(getserial())

sense = SenseHat()
sense.clear()

thirty = datetime.timedelta(seconds=3) + datetime.datetime.now()
thirty2 = datetime.timedelta(seconds=0) + datetime.datetime.now()
thirty3 = datetime.timedelta(seconds=0) + datetime.datetime.now()
now = datetime.datetime.now()

summationOfTimeMoving = 0
steps = 0


def sendRequest(url, paramas):
    r = requests.post(url, headers={'identifier': getserial()},
                      data=paramas)
    print(r)

while 1:

    o = sense.get_orientation()
    temp = sense.get_temperature()
    humidity = sense.get_humidity()
    acceleration = sense.get_accelerometer_raw()

    gyrox = sense.get_gyroscope_raw()

    x1 = abs(gyrox['x'])
    x2 = abs(gyrox['y'])
    x3 = abs(gyrox['z'])

    x = acceleration['x']
    y = acceleration['y']
    z = acceleration['z']

    if datetime.datetime.now() >= thirty:
        # print("request : {0}".format(g))
        try:
            thread.start_new_thread(sendRequest, (
                'http://172.16.0.49:4242/informations', {'temperature': temp, 'humidity': humidity}))
        except:
            print ("Error: unable to start thread")
        thirty = datetime.timedelta(seconds=3) + datetime.datetime.now()

    if x > 1.2 or y > 1.2 or z > 1.2:


        start = datetime.datetime.now()

        try:
            thread.start_new_thread(sendRequest, (
                'http://172.16.0.49:4242/alert', {'accelx': x, 'accely': y, 'accelz': z}))
        except:
            print ("Error: unable to start thread")

        if x1 >= 0.02 or x2 >= 0.02 or x3 >= 0.02:
            steps = steps + 1

        print("start moving")
        while x1 >= 0.02 or x2 >= 0.02 or x3 >= 0.02:


            gyrox = sense.get_gyroscope_raw()
            x1 = abs(gyrox['x'])
            x2 = abs(gyrox['y'])
            x3 = abs(gyrox['z'])


            if datetime.datetime.now() >= thirty3:
                try:
                    thread.start_new_thread(sendRequest, (
                        'http://172.16.0.49:4242/updateGiroscope', {'x': x1, 'y': x2, 'z': x3, 'x1': x, 'x2': y, 'x3': z}))
                except:
                    print ("Error: unable to start thread")
                thirty3 = datetime.timedelta(seconds=0.5) + datetime.datetime.now()

        end = datetime.datetime.now()
        print("end moving")

        differernceInTime = abs(end.second - start.second)
        summationOfTimeMoving += differernceInTime
        # sumOfTime = summationOfTimeMoving + differernceInTime
        if differernceInTime >= 1:
            try:
                thread.start_new_thread(sendRequest, (
                    'http://172.16.0.49:4242/alertStop',
                    {'time': differernceInTime, 'sumOfTime': summationOfTimeMoving, 'steps': steps}))
            except:
                print ("Error: unable to start thread")

    if datetime.datetime.now() >= thirty2:
        try:
            thread.start_new_thread(sendRequest, (
                'http://172.16.0.49:4242/updateGiroscope', {'x': x1, 'y': x2, 'z': x3, 'x1': x, 'x2': y, 'x3': z}))
        except:
            print ("Error: unable to start thread")
        thirty2 = datetime.timedelta(seconds=0.5) + datetime.datetime.now()

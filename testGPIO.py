from periphery import GPIO
import time

on_off = GPIO(7, 'in')
disallowed_img = GPIO(138, 'in')
photoSensor = GPIO(140, 'in')
redLight = GPIO(8, 'out')
greenLight = GPIO(141, 'out')


while True:

    print("On/off: {}    not approved: {}   Photo sensor: {}".format(on_off.read(), disallowed_img.read(), photoSensor.read()))
    time.sleep(0.3)


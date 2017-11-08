from yowsup.stacks import YowStackBuilder
from yowsup.layers.auth import AuthError
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from layer import EchoLayer
from controller.databaseorm import DatabaseOrm as db
from yowsup.layers.axolotl.props import PROP_IDENTITY_AUTOTRUST
import time
import datetime

CREDENTIALS = ("584241284028", "NzTpLXj0b516w8Eqm5zh+FP5PC8=")


class YowsupEchoStack(object):
    def __init__(self, credentials, encryptionEnabled = True):
        stackBuilder = YowStackBuilder()

        self.stack = stackBuilder\
            .pushDefaultLayers(encryptionEnabled)\
            .push(EchoLayer)\
            .build()

        self.stack.setCredentials(credentials)
        self.stack.setProp(PROP_IDENTITY_AUTOTRUST, True)

    def start(self):
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        try:
            self.stack.loop()
        except AuthError as e:
            print("Authentication Error: %s" % e.message)

if __name__ == '__main__':
    db().initialize()

    st = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
    print(">>>>>> Starting at %s" % st)

    while True:

        print(">>>>>> Loop start")
        try:
            YowsupEchoStack(CREDENTIALS).start()
        except Exception as e:
            print("Exception occurred at core level..."+str(e))

        print("Will try to reboot in 10s")
        time.sleep(10)

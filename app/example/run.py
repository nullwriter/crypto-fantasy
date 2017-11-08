from yowsup.stacks import YowStackBuilder
from yowsup.layer import EchoLayer
from yowsup.layers.auth import AuthError
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from yowsup.env import YowsupEnv

credentials = ("584142534221", "adsjMa8PHATaS4e0lDhy8qe1MjU=")  # replace with your phone and password

if __name__ == "__main__":
    stackBuilder = YowStackBuilder()

    stack = stackBuilder \
        .pushDefaultLayers(True) \
        .push(EchoLayer) \
        .build()

    stack.setCredentials(credentials)
    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))  # sending the connect signal
    stack.loop()  # this is the program mainloop

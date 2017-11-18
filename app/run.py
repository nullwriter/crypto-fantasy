import traceback

from yowsup.stacks import YowStackBuilder
from yowsup.layers.auth import AuthError
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from layer import EchoLayer
from controller.databaseorm import DatabaseOrm as db
from yowsup.layers.axolotl.props import PROP_IDENTITY_AUTOTRUST
import time
import datetime


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
            print("Authentication Error: %s" % e)


def get_credentials():

    credentials_file = 'credentials.txt'

    try:
        with open(credentials_file, 'r') as f:
            data = f.read().replace('\n', '')
    except (IOError, OSError):
        print('Credentials file %s was not found. Creating %s... Please modify with login details and re-run the bot.'
              % (credentials_file, credentials_file))
        with open(credentials_file, 'w') as f:
            f.write('phone_number:password')
        exit(1)

    parts = data.split(':')
    login = (parts[0], parts[1])

    if parts[0] == 'phone_number' or parts[1] == 'password':
        raise ValueError('Default crendentials.txt detected. Please modify with login details.')

    return login

if __name__ == '__main__':
    db().initialize()

    try:
        credentials = get_credentials()
    except IndexError as e:
        print('Exception: Incorrect format in credentials file.')
        exit(1)
    except Exception as e:
        print('Exception: '+str(e))
        exit(1)

    st = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
    print(">>>>>> Starting at %s" % st)

    while True:

        print(">>>>>> Loop start")
        try:
            YowsupEchoStack(credentials).start()
        except AttributeError as e:
            print("Attr error: "+str(e))
            print(traceback.format_exc())
        except Exception as e:
            print(traceback.format_exc())
            print("Exception occurred at core level..."+str(e))

        print("Will try to reboot in 10s")
        time.sleep(10)

from click._compat import raw_input
from controller.databaseorm import DatabaseOrm as db
from controller.whatsappbot import MethodCallInterface
import time
import datetime
import traceback

FAKE_NUMBER = ""


class CmdFakeLayer:

    def __init__(self):
        self.mcall = MethodCallInterface()

    def on_message(self, message):
        message_to_send = self.mcall.resolve(
            message,
            FAKE_NUMBER,
            FAKE_NUMBER
        )

        if message_to_send:
            print(message_to_send)


if __name__ == '__main__':
    db().initialize()
    fake_layer = CmdFakeLayer()

    st = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
    print(">>>>>> Starting at %s" % st)
    print(">>>>>> Loop start")

    while True:

        try:
            user_input = raw_input("Type message: ")
            fake_layer.on_message(user_input)
        except AttributeError as e:
            print("Attr error: "+str(e))
            print(traceback.format_exc())
        except Exception as e:
            print(traceback.format_exc())
            print("Exception occurred at core level..."+str(e))

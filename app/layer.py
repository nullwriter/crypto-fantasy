from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.common.tools import Jid
from yowsup.layers.protocol_chatstate.protocolentities import OutgoingChatstateProtocolEntity
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_presence.protocolentities import UnavailablePresenceProtocolEntity
from yowsup.layers.protocol_presence.protocolentities import AvailablePresenceProtocolEntity
from controller.whatsappbot import MethodCallInterface
import threading
from random import randint
import datetime
import time


class EchoLayer(YowInterfaceLayer):

    PROP_MESSAGES = "org.openwhatsapp.yowsup.prop.sendclient.queue"  # list of (jid, message) tuples

    def __init__(self):
        super(EchoLayer, self).__init__()
        self.ackQueue = []
        self.lock = threading.Condition()
        self.mcall = MethodCallInterface()

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        self.toLower(messageProtocolEntity.ack())
        time.sleep(randint(5, 10))
        self.toLower(AvailablePresenceProtocolEntity())
        self.toLower(messageProtocolEntity.ack(True))

        if messageProtocolEntity.getType() == 'text':
            self.onTextMessage(messageProtocolEntity)  # Send the answer

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())

    def onTextMessage(self, messageProtocolEntity):

        # print messages read
        st = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
        print("[%s] Received '%s' from %s" % (
            st,
            messageProtocolEntity.getBody(),
            messageProtocolEntity.getFrom(False)
        ))

        #if messageProtocolEntity.getFrom(False) == "584142534221":

        message = messageProtocolEntity.getBody()
        message_to_send = self.mcall.resolve(
            message,
            messageProtocolEntity.getFrom(False),
            messageProtocolEntity.participant
        )

        if message_to_send:
            self.toLower(OutgoingChatstateProtocolEntity(OutgoingChatstateProtocolEntity.STATE_TYPING, Jid.normalize(
                messageProtocolEntity.getFrom(False))))  # Set is writing
            time.sleep(randint(4, 8))
            self.toLower(OutgoingChatstateProtocolEntity(OutgoingChatstateProtocolEntity.STATE_PAUSED, Jid.normalize(
                messageProtocolEntity.getFrom(False))))  # Set no is writing
            time.sleep(randint(4, 8))

            self.toLower(TextMessageProtocolEntity(message_to_send, to=messageProtocolEntity.getFrom()))

        time.sleep(randint(4, 8))
        self.toLower(UnavailablePresenceProtocolEntity())

    def onMediaMessage(self, messageProtocolEntity):
        # just print info
        if messageProtocolEntity.getMediaType() == "image":
            print("Echoing image %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.getMediaType() == "location":
            print("Echoing location (%s, %s) to %s" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude(), messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.getMediaType() == "vcard":
            print("Echoing vcard (%s, %s) to %s" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData(), messageProtocolEntity.getFrom(False)))

# @ProtocolEntityCallback("success")
# def onSuccess(self, successProtocolEntity):
#     self.lock.acquire()
#     for target in self.getProp(self.__class__.PROP_MESSAGES, []):
#         phone, message = target
#         if '@' in phone:
#             messageEntity = TextMessageProtocolEntity(message, to = phone)
#         elif '-' in phone:
#             messageEntity = TextMessageProtocolEntity(message, to = "%s@g.us" % phone)
#         else:
#             messageEntity = TextMessageProtocolEntity(message, to = "%s@s.whatsapp.net" % phone)
#         print(phone)
#         self.ackQueue.append(messageEntity.getId())
#         self.toLower(messageEntity)
#     self.lock.release()
#
# @ProtocolEntityCallback("ack")
# def onAck(self, entity):
#     self.lock.acquire()
#     if entity.getId() in self.ackQueue:
#         self.ackQueue.pop(self.ackQueue.index(entity.getId()))
#
#     if not len(self.ackQueue):
#         self.lock.release()
#         raise KeyboardInterrupt()
#
#     self.lock.release()

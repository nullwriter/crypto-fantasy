from domain.tradingexceptions import NoPersonWasFoundError, YouAreAlreadyRegisteredError
from service.getperson import GetPerson
from service.persistregister import PersistRegister


class RegisterAction:

    def __init__(self, phone, name):
        self.phone_number = phone
        self.name = name

        if name is None:
            raise ValueError("You must provide a name to register. e.g. register Barack Obama")

    def persist(self):

        """
        Check if person isnt currently registered
        """
        try:
            person = GetPerson(number=self.phone_number).get()
        except NoPersonWasFoundError:
            pass
        else:
            raise YouAreAlreadyRegisteredError

        PersistRegister().persist(self)
        return self.name+", you have been successfully registered"

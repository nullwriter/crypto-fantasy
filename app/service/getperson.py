from domain.tradingexceptions import NoPersonWasFoundError
from domain.tabledef import Person
from service.contextmanager import session_scope


class GetPerson:

    def __init__(self, number=""):
        self.phone_number = number

    def get(self):

        with session_scope() as session:
            person = session.query(Person).filter_by(phone_number=self.phone_number).first()

        if person is None:
            raise NoPersonWasFoundError

        return person

    def get_by_id(self, id):

        with session_scope() as session:
            person = session.query(Person).filter_by(id=id).first()

        return person
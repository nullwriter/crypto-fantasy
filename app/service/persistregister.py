from domain.tabledef import Person
from service.contextmanager import session_scope


class PersistRegister:

    def __init__(self):
        pass

    def persist(self, action):

        person = Person(
            name=action.name,
            phone_number=action.phone_number,
            authorized=True
        )

        with session_scope() as session:
            session.add(person)

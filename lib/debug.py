from models.__init__ import CONN, CURSOR
from models.user import User
import ipdb


def reset_database():
    User.drop_table()
    User.create_table()


    karen = User.create("Karen")
    leroy = User.create("Leroy")
    lucy = User.create("Lucy")
    herold = User.create("Herold")


reset_database()
ipdb.set_trace()
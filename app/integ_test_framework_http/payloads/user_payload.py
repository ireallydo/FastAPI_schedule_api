import random
import string
from sorcery import dict_of
from random_words import RandomWords

from settings.settings import Settings
from ..dto import CreateUserRequest


settings = Settings()


# def random_sex():
#     options = ["male", "female"]
#     return random.choice(options)

# def random_date_str():
#     date = ''.join(str(random.randint(1995, 2010)) + '-' + str(random.randint(1, 12)) + '-' + str(random.randint(1, 28)))
#     return date

def fake_email():
    email = ''.join(random.choice(string.ascii_lowercase) for i in range(7)) + '@fakemail.com'
    return email

def random_login():
    # https://randomwords.readthedocs.io/en/latest/how_to_use.html
    r = RandomWords()
    new_login = 'U_' + r.random_word() + '_' + r.random_word()
    return new_login


def create_user():
    payload = CreateUserRequest(**dict_of(login=random_login(), password=settings.TEST_PASSWORD, email=fake_email())).json()
    return payload

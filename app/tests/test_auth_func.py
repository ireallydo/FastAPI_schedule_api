import unittest
from fastapi import Depends
from sqlalchemy.orm import Session

from db import SessionLocal, engine
from crud import get_user, get_user_by_email, get_users
#from main import get_db

def get_db():
    db = SessionLocal();
    try:
        yield db;
    finally:
        db.close();

class TestGetUser(unittest.TestCase):

    def test_get_existent_user(self):
        self.assertEqual(get_user(db = Depends(get_db), user_id = 1), (NULL, NULL, 1, 'johndoe', 'johndoe@example.com', 'fakehashedpassword1', 0, NULL, NULL, NULL), 'Should be John Doe')

if __name__ == '__main__':
    unittest.main()

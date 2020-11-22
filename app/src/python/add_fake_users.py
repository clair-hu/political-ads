import sqlalchemy
import pymysql
from sqlalchemy.orm import sessionmaker
from sqlalchemy_declarative import Base
import random
import string

engine = sqlalchemy.create_engine(
    'mysql+pymysql://root:windymarker@/us_political_ads')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)


def random_user_name():
    length = 30
    letters = string.ascii_lowercase
    name = ''.join(random.choice(letters) for i in range(length))
    return name


def register(candidate_id):
    firebase_id = random_user_name()
    user_name = random_user_name()
    queries = [
        """
    INSERT INTO users(user_name, is_official)
    VALUES ('%s', false);
    """ % (user_name),
        """
    INSERT INTO firebase_users(user_id, firebase_id)
    SELECT user_id, '%s' 
    FROM users WHERE users.user_name = '%s';
    """ % (firebase_id, user_name),
        """
    INSERT INTO mimics(user_id, candidate_id)
    SELECT user_id, %d
    FROM users WHERE users.user_name = '%s';
    """ % (candidate_id, user_name),
        """
    INSERT INTO balances(user_id, balance)
    SELECT new_user.user_id, candidate_balance.total
    FROM (SELECT user_id FROM users WHERE users.user_name = '%s') new_user,
        (SELECT SUM(spending) AS total FROM spendings WHERE user_id = %d GROUP BY user_id) candidate_balance;
    """ % (user_name, candidate_id),
        """
    INSERT INTO spendings
    SELECT new_user.user_id as user_id, all_regions.region_id as region_id, 0 as spending
    FROM (SELECT user_id FROM users WHERE users.user_name = '%s') new_user,
        (SELECT region_id FROM regions) all_regions;
        """ % (user_name)
    ]
    for query in queries:
        results = engine.execute(query)


count = int(input("Number of users (>0): "))
mimics = int(input("Mimic id [1, 10]: "))

assert (mimics >= 1 and mimics <= 10)
assert (count >= 1)

for i in range(count):
    register(mimics)

-- Given a firebase ID and a candidate, create data for a new user.
-- Get spending that a candidate has done.
-- Example Input: firebase ID: 100, User Name: helloworld123, Candidate ID: 1

INSERT INTO users(user_name, is_official)
VALUES ("helloworld123", false);

INSERT INTO firebase_users(user_id, firebase_id)
SELECT user_id, 100 
FROM users WHERE users.user_name = "helloworld123";

INSERT INTO mimics(user_id, mimics)
SELECT user_id, 1 
FROM users WHERE users.user_name = "helloworld123";

INSERT INTO spendings(user_id, region_id, spending)
VALUES (11, 1, 2500),
        (11, 5, 3000),
        (11, 20, 1900);

INSERT INTO balances(user_id, balance)
SELECT new_user.user_id, candidate_balance.total
FROM (SELECT user_id FROM users WHERE users.user_name = "helloworld123") new_user,
     (SELECT SUM(spending) AS total FROM spendings GROUP BY user_id WHERE user_id = 1) candidate_balance;


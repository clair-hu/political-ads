CREATE TABLE users
  (
     user_id     INT NOT NULL auto_increment,
     user_name   VARCHAR(500) NOT NULL,
     is_official BOOLEAN NOT NULL,
     PRIMARY KEY(user_id)
  );

CREATE INDEX is_official ON users(is_official);

CREATE TABLE regions
  (
     region_id   INT NOT NULL auto_increment,
     region_name VARCHAR(100) NOT NULL,
     vote_num INT NOT NULL,
     PRIMARY KEY(region_id)
  );

CREATE TABLE balances
  (
     user_id INT NOT NULL,
     balance INT NOT NULL,
     FOREIGN KEY(user_id) REFERENCES users(user_id)
  );

CREATE TABLE spendings
  (
     user_id   INT NOT NULL,
     region_id INT NOT NULL,
     spending  INT NOT NULL,
     PRIMARY KEY(user_id, region_id),
     FOREIGN KEY(user_id) REFERENCES users(user_id),
     FOREIGN KEY(region_id) REFERENCES regions(region_id)
  );

CREATE TABLE mimics
  (
    user_id  INT NOT NULL,
    candidate_id   INT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(candidate_id) REFERENCES users(user_id)
  );

CREATE INDEX mimic_candidate_id ON mimics(candidate_id);

CREATE TABLE firebase_users
  (
    user_id INT NOT NULL,
    firebase_id VARCHAR(100) NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
  );

CREATE TABLE challenges
  (
    challenge_id INT NOT NULL auto_increment,
    challenger_id INT NOT NULL, challengee_id INT NOT NULL,
    PRIMARY KEY(challenge_id),
    FOREIGN KEY(challenger_id) REFERENCES users(user_id),
    FOREIGN KEY(challengee_id) REFERENCES users(user_id)
  );

CREATE INDEX challenger_history ON challenges(challenger_id); 

CREATE TABLE challenge_spendings
  (
    challenge_id INT NOT NULL,
    region_id INT NOT NULL,
    challenger_spending INT NOT NULL,
    challengee_spending INT NOT NULL,
    PRIMARY KEY(challenge_id, region_id),
    FOREIGN KEY(challenge_id) REFERENCES challenges(challenge_id),
    FOREIGN KEY(region_id) REFERENCES regions(region_id)
  );


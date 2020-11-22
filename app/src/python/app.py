from flask import Flask, make_response, request, jsonify, abort
import sqlalchemy
import pymysql
from sqlalchemy_declarative import Base, User, Regions, Balances, Spendings, Mimics, FirebaseUsers
from sqlalchemy.orm import sessionmaker
from flask_cors import CORS, cross_origin

import sys

engine = sqlalchemy.create_engine(
    'mysql+pymysql://root:windymarker@/us_political_ads')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

@app.errorhandler(400)
def invalid_request_parameters(e):
    return jsonify(error=str(e)), 400

def respond(msg):
    r = make_response(msg)
    r.headers['Access-Control-Allow-Origin'] = '*'
    r.headers['X-Content-Type-Options'] = 'nosniff'
    return r

@app.route("/register", methods=['POST'])
def register():
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://root:windymarker@/us_political_ads')
    content = request.get_json()
    print(content)
    firebase_id = content['firebase_id']
    user_name = content['user_name']
    candidate_id = content['candidate_id']
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
    SELECT new_user.user_id, region_id, 0 
    FROM regions, (SELECT user_id FROM users WHERE users.user_name = '%s') new_user;
    """ % (user_name)
    ]
    for query in queries:
        results = engine.execute(query)
        print(query)
        print(results)
    return respond("Successfully added user.")


@app.route("/official-candidates", methods=['GET'])
def get_official_candidates():
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://root:windymarker@/us_political_ads')
    query = "SELECT user_id, user_name FROM users WHERE is_official = true ORDER BY user_id;"
    results = engine.execute(query)
    data = []
    for user_id, user_name in results:
        user = {}
        user.update({'user_id': user_id})
        user.update({'user_name': user_name})
        data.append(user)
    return jsonify(candidates=data)


# give a firebase ID, get user information
@app.route("/user-information", methods=['GET'])
def get_user_information():
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://root:windymarker@/us_political_ads')
    firebase_id = request.args.get('firebase_id')
    query = "SELECT users.user_id, users.user_name FROM users INNER JOIN firebase_users ON firebase_users.user_id = users.user_id WHERE firebase_users.firebase_id = '%s';" % firebase_id
    results = engine.execute(query)

    user = {}
    for user_id, user_name in results:
        user.update({'user_id': user_id})
        user.update({'user_name': user_name})

    return jsonify(user=user)


@app.route("/mimics", methods=['GET'])
def get_mimics():
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://root:windymarker@/us_political_ads')
    user_id = request.args.get('user_id')
    query = "SELECT candidate_id, user_id from mimics where user_id = '%s';" % user_id
    results = engine.execute(query)
    data = {}
    for candidate_id, user_id in results:
        data.update({'mimics': candidate_id})

    return jsonify(data=data)

@app.route("/mimickers", methods=['GET'])
def get_mimickers():
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://root:windymarker@/us_political_ads')
    candidate_id = request.args.get('candidate_id')
    query = "SELECT mimics.user_id as user_id, users.user_name as user_name from mimics JOIN users ON mimics.user_id = users.user_id where candidate_id = '%s';" % candidate_id
    results = engine.execute(query)
    data = []
    for user_id, user_name in results:
        data.append({'user_id': user_id, 'user_name':user_name })

    return jsonify(data=data)
@app.route("/user-spending", methods=['GET'])
def get_user_spending():
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://root:windymarker@/us_political_ads')
    user_id = request.args.get('user_id')
    query = "SELECT region_name, spendings.region_id, spending FROM spendings INNER JOIN regions ON spendings.region_id = regions.region_id WHERE user_id = '%s';" % user_id
    results = engine.execute(query)
    spendings = []
    for region_name, region_id, spending in results:
        region = {}
        region.update({'region': region_name})
        region.update({'region_id': region_id})
        region.update({'value': spending})
        spendings.append(region)

    return jsonify(spendings=spendings)


@app.route("/user-spending-heatmap", methods=['GET'])
def get_user_spending_for_heatmap():
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://root:windymarker@/us_political_ads')
    user_id = request.args.get('user_id')
    query = "SELECT region_name, spending FROM (SELECT * from spendings WHERE user_id = '%s') a RIGHT JOIN regions ON a.region_id = regions.region_id;" % user_id
    results = engine.execute(query)

    total_spending = 0
    original_data = {}
    SKIP_REGIONS = [
        'Guam', 'American Samoa', 'Northern Mariana Islands', 'Puerto Rico',
        'Unknown', 'Virgin Islands(U.S.)'
    ]
    for region_name, spending in results:
        if region_name in SKIP_REGIONS:
            continue
        if spending is None:
            spending = 0
        total_spending += spending
        original_data.update({region_name: spending})

    scaled_data = {}
    for key in original_data:
        scaled_data.update({
            key:
            0 if total_spending == 0 else 100 * original_data[key] / total_spending
        })

    return jsonify(data=scaled_data)

@app.route("/average-mimic-spending-heatmap", methods=['GET'])
def get_average_mimic_spending_heatmap():
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://root:windymarker@/us_political_ads')
    candidate_id = request.args.get('candidate_id')
    query = "SELECT region_name, avg from (SELECT region_id, AVG(spending) as avg from (SELECT * from mimics where candidate_id = '%s') a inner join spendings on a.user_id = spendings.user_id GROUP BY region_id) b right join regions on b.region_id = regions.region_id;" % candidate_id
    results = engine.execute(query)

    total_spending = 0
    original_data = {}
    SKIP_REGIONS = [
        'Guam', 'American Samoa', 'Northern Mariana Islands', 'Puerto Rico',
        'Unknown', 'Virgin Islands(U.S.)'
    ]
    for region_name, spending in results:
        if region_name in SKIP_REGIONS:
            continue
        if spending is None:
            spending = 0

        total_spending += spending
        original_data.update({region_name: spending})

    scaled_data = {}
    for key in original_data:
        scaled_data.update({
            key:
            0 if total_spending == 0 else 100 * original_data[key] / total_spending
        })

    return jsonify(data=scaled_data)

@app.route("/update-spending", methods=['PUT'])
def update_spending():
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://root:windymarker@/us_political_ads')
    content = request.get_json()
    user_id = content['user_id']
    region_id = content['region_id']
    value = content['value']
    # get original money spent in that region
    query = """
    SELECT IFNULL(( SELECT
        spending
        FROM spendings
        where user_id = %d and region_id = %d
    ), 0) AS spending;
    """ % (user_id, region_id)
    result = engine.execute(query)
    oldSpent = 0
    for spending in result:
        oldSpent = spending[0]
    diff = value-oldSpent
    # update balance table
    update_query = "UPDATE balances SET balance = balance - %d WHERE user_id = %d;" % (diff, user_id)
    engine.execute(update_query)
    query = "INSERT INTO spendings(user_id, region_id, spending) VALUES(%d, %d, %d) ON DUPLICATE KEY  UPDATE spending = %d;" % (
        user_id, region_id, value, value)
    results = engine.execute(query)
    return respond("Successfully updated user spendings.")


@app.route("/regions", methods=['GET'])
def get_regions():
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://root:windymarker@/us_political_ads')
    query = "SELECT region_name, region_id from regions;"
    results = engine.execute(query)

    data = []
    for region_name, region_id in results:
        region = {}
        region.update({'region_name': region_name})
        region.update({'region_id': region_id})
        data.append(region)

    return jsonify(regions=data)


@app.route("/userbase-stats", methods=['GET'])
def userbase_stats():
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://root:windymarker@/us_political_ads')
    query = "SELECT user_name, count from (SELECT candidate_id, COUNT(*) as count from mimics group by candidate_id) a INNER JOIN users ON a.candidate_id= users.user_id;"
    results = engine.execute(query)

    data = []
    for candidate_name, count in results:
        result = {}
        result.update({'candidate_name': candidate_name})
        result.update({'count': count})
        data.append(result)

    return jsonify(data=data)

@app.route("/challenge-history", methods=['GET'])
def get_challenge_history():
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://root:windymarker@/us_political_ads')
    challenge_id = request.args.get('challenge_id')
    query = "SELECT challenge_id, user_name from challenges INNER JOIN users ON challenges.challengee_id = users.user_id WHERE challenge_id = '%s';" % challenge_id
    results = engine.execute(query)
    data = {}
    for challenge_id, user_name in results:
        data['challengee_name'] = user_name

    query = "SELECT region_name, challenger_spending, challengee_spending, vote_num FROM challenge_spendings INNER JOIN regions ON challenge_spendings.region_id = regions.region_id where challenge_id = '%s';" % challenge_id
    results = engine.execute(query)
    spendings = []
    for region_name, challenger_spending, challengee_spending, vote_num in results:
        spendings.append({'region': region_name, 'challenger_spending': challenger_spending, 'challengee_spending':challengee_spending, 'vote_num': vote_num })
    data['results'] = spendings
    return jsonify(data=data)

@app.route("/user-challenges", methods=['GET'])
def get_user_challenges():
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://root:windymarker@/us_political_ads')
    challenger_id = request.args.get('user_id')
    query = "SELECT challenge_id, user_name from challenges INNER JOIN users ON challenges.challengee_id = users.user_id WHERE challenger_id = '%s';" % challenger_id
    results = engine.execute(query)

    data = []
    for challenge_id, user_name in results:
        query = "SELECT region_name, challenger_spending, challengee_spending, vote_num  FROM challenge_spendings INNER JOIN regions ON challenge_spendings.region_id = regions.region_id where challenge_id = '%s';" % challenge_id
        spending_results = engine.execute(query)
        spendings = []
        for region_name, challenger_spending, challengee_spending, vote_num in spending_results:
            spendings.append({'region': region_name, 'challenger_spending': challenger_spending, 'challengee_spending':challengee_spending, 'vote_num': vote_num })
        data.append({'challenge_id': challenge_id, 'challengee_name': user_name, 'results': spendings })
    return jsonify(data=data)

@app.route("/balance", methods=['GET'])
def get_balance():
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://root:windymarker@/us_political_ads')
    user_id = request.args.get('user_id')
    query = "SELECT balance, user_id from balances where user_id = '%s';" % user_id
    results = engine.execute(query)
    data = {}
    for balance, user_id in results:
        print(balance)
        data.update({'balance': balance, 'user_id': user_id})
    return jsonify(data=data)

@app.route("/create-challenge", methods=['POST'])
def issue_challenge():
    engine = sqlalchemy.create_engine(
        'mysql+pymysql://root:windymarker@/us_political_ads')
    content = request.get_json()
    challenger_id = content['challenger_id']
    challengee_name = content['challengee_name']
    challenger_mimics_query = "SELECT candidate_id, user_id FROM mimics WHERE user_id = '%s';" % challenger_id;
    challengee_mimics_query = "SELECT candidate_id, mimics.user_id FROM mimics INNER JOIN users ON mimics.user_id = users.user_id WHERE user_name = '%s';" % challengee_name;
    results = engine.execute(challenger_mimics_query);
    for mimics, user_id in results:
        challenger_mimics = mimics
    results = engine.execute(challengee_mimics_query);
    for mimics, user_id in results:
        challengee_mimics = mimics
        challengee_id = user_id

    if challenger_mimics != challengee_mimics:
        abort(400, description="Challenger mimics does not match Challengee mimics")

    add_challenge_query = "INSERT INTO challenges(challenger_id, challengee_id) VALUES('%s', '%s');" % (challenger_id, challengee_id)
    results = engine.execute(add_challenge_query)
    get_challenge_id_query = "SELECT LAST_INSERT_ID(), 1";
    results = engine.execute(get_challenge_id_query)
    for cid, tmp in results:
        challenge_id = cid

    populate_challenge_spending = "INSERT INTO challenge_spendings SELECT '%s', a.region_id as region_id, a.spending AS challenger_spending, b.spending AS challengee_spending FROM spendings a INNER JOIN spendings b ON a.region_id = b.region_id WHERE a.user_id = '%s' AND b.user_id = '%s';" % (challenge_id, challenger_id, challengee_id)
    results = engine.execute(populate_challenge_spending)
    return respond("Successfully issued new challenge")

if __name__ == "__main__":
    app.run()

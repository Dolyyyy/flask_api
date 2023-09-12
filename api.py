from urllib import request

from flask import Flask, jsonify, redirect, request, url_for
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Row

app = Flask(__name__)

engine = create_engine('mysql+pymysql://user:password@localhost/database')

@app.route('/', methods=['GET'])
def apiredirector():
    return redirect('/api')

@app.route('/api/', methods=['GET'])
def getapi():
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            if rule.arguments:
                continue

            url = f"{request.scheme}://{request.host}{url_for(rule.endpoint)}"
            route = {
                'route': str(rule),
                'methods': ','.join(rule.methods),
                'endpoint': rule.endpoint,
                'url': url
            }
            routes.append(route)
    return jsonify({'routes': routes})

@app.route('/api/users', methods=['GET'])
def getusers():
    try:
        count_query = text("SELECT COUNT(*) as counter FROM users")
        conn = engine.connect()
        count_result = conn.execute(count_query)
        counter = count_result.scalar()

        users_query = text("SELECT * FROM users")
        users_result = conn.execute(users_query)
        user_data = [dict(zip(users_result.keys(), row)) for row in users_result]

        conn.close()

        if user_data:
            return jsonify({"count": counter, "data": user_data})
        else:
            return jsonify({'message': 'Aucun résultat trouvé pour cette route.'})
    except Exception as e:
        return jsonify({'message': "Une erreur s'est produite durant la requête."})


@app.route('/api/users/license/<license>', methods=['GET'])
def getbylicense(license):
    try:
        query = text("SELECT * FROM users WHERE license = :license")
        conn = engine.connect()
        result = conn.execute(query, {'license': license})
        column_names = result.keys()
        user_data = [dict(zip(column_names, row)) for row in result]
        conn.close()
        if user_data:
            return jsonify({"data": user_data})
        else:
            return jsonify({'message': 'Aucun résultat trouvé pour cette route.'})
    except Exception as e:
        return jsonify({'message': "Une erreur s'est produite durant la requête."})

@app.route('/api/users/name/<name>', methods=['GET'])
def getbyname(name):
    try:
        query = text("SELECT * FROM users WHERE name = :name")
        conn = engine.connect()
        result = conn.execute(query, {'name': name})
        column_names = result.keys()
        user_data = [dict(zip(column_names, row)) for row in result]
        conn.close()
        if user_data:
            return jsonify({"data": user_data})
        else:
            return jsonify({'message': 'Aucun résultat trouvé pour cette route.'})
    except Exception as e:
        return jsonify({'message': "Une erreur s'est produite durant la requête."})

@app.route('/api/users/steam/<steam>', methods=['GET'])
def getbysteam(steam):
    try:
        query = text("SELECT * FROM users WHERE identifier = :steam")
        conn = engine.connect()
        result = conn.execute(query, {'steam': steam})
        column_names = result.keys()
        user_data = [dict(zip(column_names, row)) for row in result]
        conn.close()
        if user_data:
            return jsonify({"data": user_data})
        else:
            return jsonify({'message': 'Aucun résultat trouvé pour cette route.'})
    except Exception as e:
        return jsonify({'message': "Une erreur s'est produite durant la requête."})

@app.route('/api/users/group/<group>', methods=['GET'])
def getbygroup(group):
    try:
        query = text("SELECT * FROM users WHERE `group` = :group")
        conn = engine.connect()
        result = conn.execute(query, {'group': group})
        column_names = result.keys()
        user_data = [dict(zip(column_names, row)) for row in result]
        conn.close()
        if user_data:
            return jsonify({"data": user_data})
        else:
            return jsonify({'message': 'Aucun résultat trouvé pour cette route.'})
    except Exception as e:
        return jsonify({'message': "Une erreur s'est produite durant la requête."})

@app.route('/api/leaderboard', methods=['GET'])
def getboard():
    try:
        query = text("SELECT * FROM leaderboard ORDER BY kills DESC")
        conn = engine.connect()
        result = conn.execute(query)
        data = [dict(zip(result.keys(), row)) for row in result]
        conn.close()
        return jsonify({"data": data})
    except Exception as e:
        return jsonify({'message': "Une erreur s'est produite durant la requête."})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9745, debug=True)
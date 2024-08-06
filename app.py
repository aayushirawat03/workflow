from flask import Flask, request, jsonify, make_response
import jwt
import datetime
import modledb

app = Flask(__name__)
app.config['SECRET_KEY'] = '381836fe163039ab7bcd0a84bf54dded9fbd4269'

modledb.init_db()

def generate_token(username):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow(),
        'sub': username
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token

@app.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({'message': 'Content type must be JSON'})

    data = request.json
    firstname = data['Firstname']
    lastname = data['lastame']
    PhoneNumber = data['PhoneNumber']
    username = data['username']
    password = data['password']

    if modledb.register_user(username, password):
        return jsonify({'message': 'Successfully registered'})
    else:
        return jsonify({'message': 'User already exists!'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = modledb.get_user(username)

    if user and user[2] == password:
        token = generate_token(username)
        response = jsonify({'token': token})
        response.set_cookie('token', token)
        return response
    else:
        return jsonify({'message': 'Invalid username or password'})

@app.route('/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({'message': 'Logged out successfully'}))
    response.set_cookie('token', '', expires=0)
    return response

if __name__ == '__main__':
    app.run(debug=True)
